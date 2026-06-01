#!/usr/bin/env python3
"""
Repair Jupyter notebooks for GitHub Preview / nbconvert compatibility.

Usage:
    python fix_notebooks.py [--root DIR] [--dry-run] [--report REPORT.md]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import nbformat
    from nbformat import NotebookNode
    from nbformat.validator import NotebookValidationError, normalize, validate
except ImportError:
    print("ERROR: nbformat is required. Install with: pip install nbformat", file=sys.stderr)
    sys.exit(1)

MERGE_CONFLICT_RE = re.compile(r"^<<<<<<<|^=======|^>>>>>>>", re.MULTILINE)
MAX_OUTPUT_BYTES = 1_000_000  # 1 MB per output blob (GitHub-safe)
TARGET_NBFORMAT = 4
TARGET_NBFORMAT_MINOR = 5

GITHUB_SAFE_MIMES = {
    "text/plain",
    "text/html",
    "text/markdown",
    "text/latex",
    "image/png",
    "image/jpeg",
    "image/svg+xml",
    "image/gif",
    "application/json",
    "application/javascript",
}

COLAB_CELL_KEYS = {"colab", "outputId"}
COLAB_NB_KEYS = {"colab", "accelerator", "gpuType", "provenance"}

IPYWIDGET_MARKERS = (
    "Upload widget is only available",
    "ipywidgets",
    'id="files-',
    "application/vnd.jupyter.widget",
)


def join_multistr(value: Any) -> str:
    """Convert Jupyter multiline string (str or list[str]) to a single str."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(str(part) for part in value)
    return str(value)


def normalize_source(source: Any) -> list[str]:
    if source is None:
        return []
    if isinstance(source, str):
        if not source:
            return []
        return source.splitlines(keepends=True) if "\n" in source else [source]
    if isinstance(source, list):
        return [str(line) for line in source]
    return [str(source)]


def output_size(output: dict) -> int:
    total = 0
    for key in ("text", "data", "traceback"):
        val = output.get(key)
        if val is None:
            continue
        if isinstance(val, dict):
            for v in val.values():
                total += len(join_multistr(v).encode("utf-8", errors="replace"))
        elif isinstance(val, list):
            total += len(join_multistr(val).encode("utf-8", errors="replace"))
        else:
            total += len(str(val).encode("utf-8", errors="replace"))
    return total


def is_ipywidget_output(output: dict) -> bool:
    data = output.get("data") or {}
    blob = " ".join(join_multistr(data.get(mime, "")) for mime in data)
    blob += join_multistr(output.get("text", ""))
    return any(marker in blob for marker in IPYWIDGET_MARKERS)


def sanitize_output(output: dict, cell_index: int, out_index: int) -> tuple[dict | None, list[str]]:
    """Return sanitized output or None to drop it; second value is fix messages."""
    fixes: list[str] = []
    out = deepcopy(output)
    otype = out.get("output_type")

    if otype not in ("stream", "display_data", "execute_result", "error"):
        fixes.append(f"cell {cell_index} output {out_index}: removed invalid output_type={otype!r}")
        return None, fixes

    if otype == "stream":
        name = out.get("name")
        if name not in ("stdout", "stderr"):
            out["name"] = "stdout"
            fixes.append(f"cell {cell_index} output {out_index}: fixed stream name -> stdout")
        out["text"] = join_multistr(out.get("text", ""))
        if "data" in out:
            del out["data"]
    elif otype == "error":
        for key in ("ename", "evalue", "traceback"):
            if key not in out:
                fixes.append(f"cell {cell_index} output {out_index}: incomplete error output removed")
                return None, fixes
        out["traceback"] = [join_multistr(line) for line in out["traceback"]]
    else:
        data = out.get("data")
        if not isinstance(data, dict):
            fixes.append(f"cell {cell_index} output {out_index}: missing/invalid data removed")
            return None, fixes
        cleaned: dict[str, str] = {}
        for mime, val in data.items():
            if mime.startswith("application/vnd."):
                fixes.append(f"cell {cell_index} output {out_index}: stripped mime {mime}")
                continue
            if mime not in GITHUB_SAFE_MIMES:
                fixes.append(f"cell {cell_index} output {out_index}: stripped unsafe mime {mime}")
                continue
            cleaned[mime] = join_multistr(val)
        if not cleaned:
            fixes.append(f"cell {cell_index} output {out_index}: empty data after sanitize removed")
            return None, fixes
        out["data"] = cleaned
        if otype == "execute_result" and "execution_count" not in out:
            out["execution_count"] = None
            fixes.append(f"cell {cell_index} output {out_index}: added execution_count to execute_result")

    if is_ipywidget_output(out):
        fixes.append(f"cell {cell_index} output {out_index}: removed ipywidgets/colab widget output")
        return None, fixes

    if output_size(out) > MAX_OUTPUT_BYTES:
        fixes.append(
            f"cell {cell_index} output {out_index}: removed oversized output "
            f"({output_size(out) // 1024} KB)"
        )
        return None, fixes

    if "attachments" in out:
        del out["attachments"]
        fixes.append(f"cell {cell_index} output {out_index}: removed attachments")

    return out, fixes


def sanitize_cell(cell: dict, cell_index: int) -> tuple[dict, list[str]]:
    fixes: list[str] = []
    c = deepcopy(cell)

    if "cell_type" not in c or c["cell_type"] not in ("code", "markdown", "raw"):
        fixes.append(f"cell {cell_index}: invalid cell_type repaired to markdown")
        c["cell_type"] = "markdown"

    if "metadata" not in c or not isinstance(c["metadata"], dict):
        c["metadata"] = {}
        fixes.append(f"cell {cell_index}: added metadata dict")
    else:
        for key in list(c["metadata"]):
            if key in COLAB_CELL_KEYS:
                del c["metadata"][key]
                fixes.append(f"cell {cell_index}: removed colab metadata key {key!r}")

    if "source" not in c:
        c["source"] = []
        fixes.append(f"cell {cell_index}: added empty source")
    c["source"] = normalize_source(c["source"])

    if "id" not in c or not isinstance(c.get("id"), str) or not c["id"]:
        c["id"] = str(uuid.uuid4())
        fixes.append(f"cell {cell_index}: added cell id")

    if c["cell_type"] == "code":
        if "outputs" not in c or not isinstance(c["outputs"], list):
            c["outputs"] = []
            fixes.append(f"cell {cell_index}: added outputs list")
        if "execution_count" not in c:
            c["execution_count"] = None
            fixes.append(f"cell {cell_index}: added execution_count")
        elif c["execution_count"] is not None and not isinstance(c["execution_count"], int):
            c["execution_count"] = None
            fixes.append(f"cell {cell_index}: reset invalid execution_count")

        new_outputs = []
        for j, out in enumerate(c["outputs"]):
            if not isinstance(out, dict):
                fixes.append(f"cell {cell_index} output {j}: removed non-dict output")
                continue
            cleaned, out_fixes = sanitize_output(out, cell_index, j)
            fixes.extend(out_fixes)
            if cleaned is not None:
                new_outputs.append(cleaned)
        c["outputs"] = new_outputs
    else:
        c.pop("outputs", None)
        c.pop("execution_count", None)

    if "attachments" in c:
        del c["attachments"]
        fixes.append(f"cell {cell_index}: removed cell attachments")

    return c, fixes


def sanitize_notebook_dict(nb: dict) -> tuple[dict, list[str], list[str]]:
    """Return (notebook, fixes, errors)."""
    fixes: list[str] = []
    errors: list[str] = []

    if not isinstance(nb, dict):
        return nb, fixes, ["root is not a JSON object"]

    nb = deepcopy(nb)
    nb["nbformat"] = TARGET_NBFORMAT
    nb["nbformat_minor"] = TARGET_NBFORMAT_MINOR

    metadata = nb.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
        fixes.append("added top-level metadata")
    for key in list(metadata):
        if key in COLAB_NB_KEYS:
            del metadata[key]
            fixes.append(f"removed notebook metadata key {key!r}")
    nb["metadata"] = metadata

    if "kernelspec" not in metadata:
        metadata["kernelspec"] = {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        }
        fixes.append("added kernelspec")
    if "language_info" not in metadata:
        metadata["language_info"] = {"name": "python", "version": "3.10.0"}
        fixes.append("added language_info")

    cells = nb.get("cells")
    if not isinstance(cells, list):
        errors.append("cells is missing or not a list")
        cells = []
    new_cells = []
    for i, cell in enumerate(cells):
        if not isinstance(cell, dict):
            errors.append(f"cell {i}: not an object — skipped")
            continue
        fixed_cell, cell_fixes = sanitize_cell(cell, i)
        fixes.extend(cell_fixes)
        new_cells.append(fixed_cell)
    nb["cells"] = new_cells

    return nb, fixes, errors


def validate_with_nbformat(nb_dict: dict) -> list[str]:
    issues: list[str] = []
    try:
        node = nbformat.from_dict(nb_dict)
        _, node = normalize(node)
        validate(node)
    except NotebookValidationError as exc:
        issues.append(f"nbformat validation: {exc}")
    except Exception as exc:
        issues.append(f"nbformat: {exc}")
    return issues


def repair_notebook_file(path: Path, dry_run: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": str(path),
        "fixed": False,
        "fixes": [],
        "errors": [],
        "remaining": [],
    }

    try:
        raw = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        result["errors"].append(f"encoding error: {exc}")
        return result

    if MERGE_CONFLICT_RE.search(raw):
        result["errors"].append("merge conflict markers found — resolve manually")
        return result

    try:
        nb = json.loads(raw)
    except json.JSONDecodeError as exc:
        result["errors"].append(f"JSON parse error: {exc}")
        return result

    nb, fixes, errors = sanitize_notebook_dict(nb)
    result["fixes"].extend(fixes)
    result["errors"].extend(errors)

    try:
        _, nb = normalize(nb)
    except Exception as exc:
        result["errors"].append(f"nbformat normalize: {exc}")
        return result

    # Re-apply GitHub-safe output shaping (normalize may convert strings back to lists).
    nb, repatch_fixes, repatch_errors = sanitize_notebook_dict(nb)
    result["fixes"].extend(repatch_fixes)
    result["errors"].extend(repatch_errors)

    remaining = validate_with_nbformat(nb)
    result["remaining"] = remaining

    if not dry_run and not result["errors"]:
        path.write_text(
            json.dumps(nb, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        result["fixed"] = True

    return result


def write_report(results: list[dict], report_path: Path) -> None:
    lines = [
        "# Notebook Repair Report",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "",
        f"**Files scanned:** {len(results)}",
        "",
    ]
    fixed = [r for r in results if r.get("fixes")]
    broken = [r for r in results if r.get("errors") or r.get("remaining")]

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Notebooks modified: {sum(1 for r in results if r.get('fixed'))}")
    lines.append(f"- Notebooks with fixes applied: {len(fixed)}")
    lines.append(f"- Notebooks with remaining issues: {len(broken)}")
    lines.append("")

    lines.append("## Per-file details")
    lines.append("")
    for r in results:
        lines.append(f"### `{r['path']}`")
        lines.append("")
        if r.get("fixes"):
            lines.append("**Fixes applied:**")
            for fix in r["fixes"]:
                lines.append(f"- {fix}")
            lines.append("")
        else:
            lines.append("- No fixes required (structure already valid).")
            lines.append("")
        if r.get("errors"):
            lines.append("**Errors:**")
            for err in r["errors"]:
                lines.append(f"- {err}")
            lines.append("")
        if r.get("remaining"):
            lines.append("**Remaining issues:**")
            for rem in r["remaining"]:
                lines.append(f"- {rem}")
            lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair Jupyter notebooks for GitHub Preview.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root")
    parser.add_argument("--dry-run", action="store_true", help="Analyze only; do not write files")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("notebook_repair_report.md"),
        help="Markdown report output path",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    notebooks = sorted(root.rglob("*.ipynb"))
    if not notebooks:
        print("No .ipynb files found.")
        return 1

    results = []
    for path in notebooks:
        if path.name.startswith("."):
            continue
        print(f"Processing {path.relative_to(root)} ...")
        results.append(repair_notebook_file(path, dry_run=args.dry_run))

    write_report(results, args.report.resolve())
    print(f"\nReport written to {args.report}")

    remaining = sum(1 for r in results if r.get("errors") or r.get("remaining"))
    if remaining:
        print(f"WARNING: {remaining} notebook(s) still have issues. See report.")
        return 2
    print("All notebooks repaired and validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

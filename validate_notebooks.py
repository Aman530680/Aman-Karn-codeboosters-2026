#!/usr/bin/env python3
"""
Validate Jupyter notebooks for GitHub Preview compatibility before commits.

Usage:
    python validate_notebooks.py [--root DIR]

Exit codes:
    0 — all notebooks pass
    1 — validation failures found
    2 — missing dependency or fatal error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import nbformat
    from nbformat.validator import NotebookValidationError, validate
except ImportError:
    print("ERROR: nbformat is required. Install with: pip install nbformat", file=sys.stderr)
    sys.exit(2)

MERGE_CONFLICT_RE = re.compile(r"^<<<<<<<|^=======|^>>>>>>>", re.MULTILINE)
MAX_OUTPUT_BYTES = 1_000_000
REQUIRED_NBFORMAT = 4
REQUIRED_NBFORMAT_MINOR = 5

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

IPYWIDGET_MARKERS = (
    "Upload widget is only available",
    "ipywidgets",
    'id="files-',
)


def join_multistr(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(str(part) for part in value)
    return str(value)


def output_size(output: dict) -> int:
    total = 0
    for key in ("text", "data", "traceback"):
        val = output.get(key)
        if isinstance(val, dict):
            for v in val.values():
                total += len(join_multistr(v).encode("utf-8", errors="replace"))
        else:
            total += len(join_multistr(val).encode("utf-8", errors="replace"))
    return total


def check_notebook(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        return [f"encoding: {exc}"]

    if MERGE_CONFLICT_RE.search(raw):
        issues.append("merge conflict markers present")

    try:
        nb = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

    if nb.get("nbformat") != REQUIRED_NBFORMAT:
        issues.append(f"nbformat must be {REQUIRED_NBFORMAT}, got {nb.get('nbformat')}")
    if nb.get("nbformat_minor") != REQUIRED_NBFORMAT_MINOR:
        issues.append(
            f"nbformat_minor must be {REQUIRED_NBFORMAT_MINOR}, got {nb.get('nbformat_minor')}"
        )

    cells = nb.get("cells")
    if not isinstance(cells, list) or not cells:
        issues.append("cells must be a non-empty list")

    for i, cell in enumerate(cells or []):
        if not isinstance(cell, dict):
            issues.append(f"cell {i}: not an object")
            continue
        for field in ("cell_type", "metadata", "source"):
            if field not in cell:
                issues.append(f"cell {i}: missing required field {field!r}")
        if "id" not in cell or not isinstance(cell.get("id"), str):
            issues.append(f"cell {i}: missing or invalid id (required for nbformat 4.5+)")

        ctype = cell.get("cell_type")
        if ctype == "code":
            if "outputs" not in cell:
                issues.append(f"cell {i}: code cell missing outputs")
            if "execution_count" not in cell:
                issues.append(f"cell {i}: code cell missing execution_count")

            for j, out in enumerate(cell.get("outputs") or []):
                if not isinstance(out, dict):
                    issues.append(f"cell {i} output {j}: not an object")
                    continue
                otype = out.get("output_type")
                if otype not in ("stream", "display_data", "execute_result", "error"):
                    issues.append(f"cell {i} output {j}: invalid output_type {otype!r}")

                if otype == "stream":
                    if not isinstance(out.get("name"), str):
                        issues.append(f"cell {i} output {j}: stream missing name")
                    text = out.get("text")
                    if text is not None and not isinstance(text, (str, list)):
                        issues.append(f"cell {i} output {j}: stream text has invalid type")
                if otype in ("display_data", "execute_result"):
                    data = out.get("data") or {}
                    for mime, val in data.items():
                        if mime.startswith("application/vnd."):
                            issues.append(f"cell {i} output {j}: forbidden mime {mime}")
                        if mime not in GITHUB_SAFE_MIMES and not mime.startswith(
                            "application/vnd."
                        ):
                            issues.append(f"cell {i} output {j}: unsafe mime {mime}")
                        if isinstance(val, list):
                            issues.append(
                                f"cell {i} output {j}: mime {mime} must be string (GitHub compat)"
                            )
                    blob = " ".join(join_multistr(v) for v in data.values())
                    if any(m in blob for m in IPYWIDGET_MARKERS):
                        issues.append(f"cell {i} output {j}: ipywidgets output not allowed")

                if output_size(out) > MAX_OUTPUT_BYTES:
                    issues.append(
                        f"cell {i} output {j}: output exceeds {MAX_OUTPUT_BYTES // 1024} KB"
                    )
                if "attachments" in out:
                    issues.append(f"cell {i} output {j}: attachments not allowed")

        if "attachments" in cell:
            issues.append(f"cell {i}: cell attachments not allowed")

        meta = cell.get("metadata") or {}
        if "colab" in meta or "outputId" in meta:
            issues.append(f"cell {i}: colab metadata should be stripped (run fix_notebooks.py)")

    try:
        node = nbformat.from_dict(nb)
        validate(node)
    except NotebookValidationError as exc:
        issues.append(f"nbformat schema: {exc}")
    except Exception as exc:
        issues.append(f"nbformat: {exc}")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate notebooks for GitHub Preview.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root")
    args = parser.parse_args()
    root = args.root.resolve()

    notebooks = sorted(root.rglob("*.ipynb"))
    if not notebooks:
        print("No .ipynb files found.")
        return 1

    failed = 0
    for path in notebooks:
        rel = path.relative_to(root)
        issues = check_notebook(path)
        if issues:
            failed += 1
            print(f"FAIL {rel}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"OK   {rel}")

    print(f"\nChecked {len(notebooks)} notebook(s).")
    if failed:
        print(f"{failed} notebook(s) failed validation.")
        print("Run: python fix_notebooks.py")
        return 1
    print("All notebooks passed GitHub compatibility checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

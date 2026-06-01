"""
Notebook Repair Script
Fixes all GitHub rendering issues across all notebooks.
"""
import json
import os
import glob
import base64
import sys

base = u"D:\\Aman-Karn-codeboosters-2026"
notebooks = glob.glob(os.path.join(base, "**", "*.ipynb"), recursive=True)

REQUIRED_KERNELSPEC = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3"
}
REQUIRED_LANGUAGE_INFO = {
    "name": "python",
    "version": "3.10.0"
}
VALID_OUTPUT_TYPES = {"stream", "display_data", "execute_result", "error"}
VALID_CELL_TYPES   = {"code", "markdown", "raw"}

MAX_IMAGE_B64_BYTES = 2 * 1024 * 1024   # 2 MB per image
MAX_TEXT_CHARS      = 50_000             # 50 K chars per text output

report = []
total_fixed = 0

def log(msg):
    report.append(msg)
    print(msg)

def fix_source(source):
    """Ensure source is a list of strings."""
    if isinstance(source, str):
        return source.splitlines(keepends=True) or [""]
    if isinstance(source, list):
        return [str(s) for s in source]
    return [""]

def fix_output(out, cell_idx, out_idx, nb_name):
    """Sanitise a single output dict. Returns (fixed_out, was_dropped)."""
    out_type = out.get("output_type", "")

    # Drop completely invalid output types
    if out_type not in VALID_OUTPUT_TYPES:
        log(f"  [DROP] {nb_name} cell {cell_idx} output {out_idx}: invalid output_type '{out_type}'")
        return None, True

    # Fix missing required keys per output type
    if out_type == "stream":
        if "name" not in out:
            out["name"] = "stdout"
        text = out.get("text", [])
        if isinstance(text, str):
            out["text"] = text.splitlines(keepends=True)
        # Truncate oversized stream output
        flat = "".join(out.get("text", []))
        if len(flat) > MAX_TEXT_CHARS:
            truncated = flat[:MAX_TEXT_CHARS]
            out["text"] = truncated.splitlines(keepends=True)
            out["text"].append(f"\n... [output truncated for GitHub rendering] ...\n")
            log(f"  [TRUNCATE] {nb_name} cell {cell_idx} output {out_idx}: stream text {len(flat)} -> {MAX_TEXT_CHARS} chars")

    elif out_type in ("display_data", "execute_result"):
        if "data" not in out:
            out["data"] = {}
        if "metadata" not in out:
            out["metadata"] = {}
        if out_type == "execute_result" and "execution_count" not in out:
            out["execution_count"] = None

        # Fix None values in data
        data = out["data"]
        for key in list(data.keys()):
            if data[key] is None:
                data[key] = "" if key != "image/png" else ""
                log(f"  [FIX] {nb_name} cell {cell_idx} output {out_idx}: null value in data['{key}'] replaced")

        # Truncate oversized text/plain
        plain = data.get("text/plain", "")
        if isinstance(plain, list):
            flat_plain = "".join(plain)
        else:
            flat_plain = str(plain)
        if len(flat_plain) > MAX_TEXT_CHARS:
            data["text/plain"] = flat_plain[:MAX_TEXT_CHARS] + "\n... [truncated] ..."
            log(f"  [TRUNCATE] {nb_name} cell {cell_idx} output {out_idx}: text/plain {len(flat_plain)} -> {MAX_TEXT_CHARS}")

        # Truncate oversized images
        img = data.get("image/png", "")
        if isinstance(img, str) and len(img) > MAX_IMAGE_B64_BYTES:
            log(f"  [CLEAR IMAGE] {nb_name} cell {cell_idx} output {out_idx}: image/png {len(img)//1024} KB > 2 MB limit — cleared")
            data.pop("image/png", None)
            data.pop("image/jpeg", None)
            data.pop("image/svg+xml", None)
            if not data:
                data["text/plain"] = "[Image output cleared — too large for GitHub rendering]"

        # Remove colab-specific intrinsic JSON (causes GitHub parse errors)
        if "application/vnd.google.colaboratory.intrinsic+json" in data:
            data.pop("application/vnd.google.colaboratory.intrinsic+json")
            log(f"  [REMOVE] {nb_name} cell {cell_idx} output {out_idx}: removed colab intrinsic JSON")

        # Remove other non-standard MIME types that break GitHub
        bad_mimes = [k for k in data if k not in (
            "text/plain", "text/html", "text/markdown",
            "image/png", "image/jpeg", "image/svg+xml",
            "application/json"
        )]
        for mime in bad_mimes:
            data.pop(mime)
            log(f"  [REMOVE MIME] {nb_name} cell {cell_idx} output {out_idx}: removed '{mime}'")

        # Sanitise text/html — remove embedded <script> tags (GitHub strips them anyway)
        html = data.get("text/html", "")
        if isinstance(html, list):
            html = "".join(html)
        if "<script" in html.lower():
            # Remove script blocks
            import re
            cleaned = re.sub(r'<script[\s\S]*?</script>', '', html, flags=re.IGNORECASE)
            data["text/html"] = cleaned.splitlines(keepends=True)
            log(f"  [CLEAN HTML] {nb_name} cell {cell_idx} output {out_idx}: removed <script> tags from text/html")

    elif out_type == "error":
        for key in ("ename", "evalue", "traceback"):
            if key not in out:
                out[key] = "" if key != "traceback" else []

    return out, False


def fix_cell(cell, cell_idx, nb_name):
    """Sanitise a single cell dict."""
    cell_type = cell.get("cell_type", "")

    # Fix invalid cell type
    if cell_type not in VALID_CELL_TYPES:
        cell["cell_type"] = "raw"
        log(f"  [FIX CELL TYPE] {nb_name} cell {cell_idx}: invalid type '{cell_type}' -> 'raw'")

    # Fix source
    cell["source"] = fix_source(cell.get("source", []))

    # Ensure metadata exists
    if "metadata" not in cell:
        cell["metadata"] = {}

    # Fix code cell specifics
    if cell_type == "code":
        if "execution_count" not in cell:
            cell["execution_count"] = None
        if "outputs" not in cell:
            cell["outputs"] = []

        fixed_outputs = []
        for j, out in enumerate(cell.get("outputs", [])):
            fixed_out, dropped = fix_output(out, cell_idx, j, nb_name)
            if not dropped:
                fixed_outputs.append(fixed_out)
        cell["outputs"] = fixed_outputs

    return cell


def fix_notebook(path):
    global total_fixed
    rel = os.path.relpath(path, base)
    nb_name = os.path.basename(path)
    fixes = 0

    with open(path, encoding="utf-8") as f:
        raw = f.read()

    # Parse JSON
    try:
        nb = json.loads(raw)
    except json.JSONDecodeError as e:
        log(f"\n[SKIP] {rel}: Invalid JSON — {e}")
        return

    changed = False

    # ── 1. Fix nbformat ──────────────────────────────────────────────────────
    if nb.get("nbformat") != 4 or nb.get("nbformat_minor", 0) < 5:
        log(f"\n[FIX] {rel}: nbformat {nb.get('nbformat')}.{nb.get('nbformat_minor')} -> 4.5")
        nb["nbformat"] = 4
        nb["nbformat_minor"] = 5
        changed = True
        fixes += 1

    # ── 2. Fix metadata ──────────────────────────────────────────────────────
    if "metadata" not in nb:
        nb["metadata"] = {}
        changed = True

    meta = nb["metadata"]

    if "kernelspec" not in meta:
        meta["kernelspec"] = REQUIRED_KERNELSPEC
        log(f"  [FIX] {rel}: added missing kernelspec")
        changed = True
        fixes += 1

    if "language_info" not in meta:
        meta["language_info"] = REQUIRED_LANGUAGE_INFO
        log(f"  [FIX] {rel}: added missing language_info")
        changed = True
        fixes += 1

    # Remove colab-specific metadata keys that can confuse GitHub renderer
    colab_keys = [k for k in meta if k in ("colab", "accelerator", "gpuClass")]
    for k in colab_keys:
        meta.pop(k)
        log(f"  [REMOVE META] {rel}: removed colab metadata key '{k}'")
        changed = True
        fixes += 1

    # ── 3. Fix cells ─────────────────────────────────────────────────────────
    cells = nb.get("cells", [])
    if not isinstance(cells, list):
        nb["cells"] = []
        log(f"  [FIX] {rel}: 'cells' was not a list — reset to empty")
        changed = True
        fixes += 1
        cells = []

    fixed_cells = []
    for i, cell in enumerate(cells):
        before = json.dumps(cell)
        cell = fix_cell(cell, i, nb_name)
        after = json.dumps(cell)
        if before != after:
            changed = True
            fixes += 1
        fixed_cells.append(cell)

    nb["cells"] = fixed_cells

    # ── 4. Save if changed ───────────────────────────────────────────────────
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        log(f"\n[SAVED] {rel} ({fixes} fix(es) applied)")
        total_fixed += 1
    else:
        log(f"\n[OK]    {rel} — no issues found")


# ── Run ───────────────────────────────────────────────────────────────────────
print("=" * 70)
print("  NOTEBOOK REPAIR SCRIPT")
print("=" * 70)

for nb_path in sorted(notebooks):
    fix_notebook(nb_path)

print("\n" + "=" * 70)
print(f"  DONE — {total_fixed}/{len(notebooks)} notebooks repaired")
print("=" * 70)

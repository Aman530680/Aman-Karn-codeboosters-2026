import json
import os
import glob
import re
import sys

base = u"D:\\Aman-Karn-codeboosters-2026"
notebooks = glob.glob(os.path.join(base, "**", "*.ipynb"), recursive=True)

print("=" * 70)
print("  NOTEBOOK DIAGNOSTIC REPORT")
print("=" * 70)

issues_found = {}

for path in notebooks:
    rel = os.path.relpath(path, base)
    file_issues = []

    # 1. Check file size
    size_kb = os.path.getsize(path) / 1024
    if size_kb > 5000:
        file_issues.append(f"LARGE FILE: {size_kb:.1f} KB (>5MB may fail GitHub render)")

    # 2. Check valid JSON
    try:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        nb = json.loads(raw)
    except json.JSONDecodeError as e:
        file_issues.append(f"INVALID JSON: {e}")
        issues_found[rel] = file_issues
        continue

    # 3. Check REAL merge conflict markers (not inside JSON strings)
    # Real conflict markers appear at the START of a line, outside JSON
    import re as _re
    real_conflict = False
    for line in raw.splitlines():
        stripped = line.strip()
        # Real git conflict lines start with <<<<<<< or >>>>>>> followed by branch name
        # or are exactly ======= on their own line (not inside a JSON string value)
        if _re.match(r'^<{7}\s', stripped) or _re.match(r'^>{7}\s', stripped):
            real_conflict = True
            break
        # ======= as a standalone line outside a JSON string
        if stripped == '=======' and not line.lstrip().startswith('"'):
            real_conflict = True
            break
    if real_conflict:
        file_issues.append("REAL MERGE CONFLICT MARKERS found in file")

    # 4. Check nbformat version
    fmt = nb.get("nbformat", 0)
    fmt_minor = nb.get("nbformat_minor", 0)
    if fmt < 4 or (fmt == 4 and fmt_minor < 5):
        file_issues.append(f"OLD NBFORMAT: {fmt}.{fmt_minor} (needs 4.5+)")

    # 5. Check metadata
    meta = nb.get("metadata", {})
    if "kernelspec" not in meta:
        file_issues.append("MISSING: kernelspec in metadata")
    if "language_info" not in meta:
        file_issues.append("MISSING: language_info in metadata")

    # 6. Check cells
    cells = nb.get("cells", [])
    if not cells:
        file_issues.append("NO CELLS found in notebook")

    for i, cell in enumerate(cells):
        cell_type = cell.get("cell_type", "unknown")

        # Check required fields
        if "source" not in cell:
            file_issues.append(f"Cell {i}: MISSING 'source' field")
        if "metadata" not in cell:
            file_issues.append(f"Cell {i}: MISSING 'metadata' field")

        # Check outputs for code cells
        if cell_type == "code":
            if "outputs" not in cell:
                file_issues.append(f"Cell {i}: MISSING 'outputs' field")
            if "execution_count" not in cell:
                file_issues.append(f"Cell {i}: MISSING 'execution_count' field")

            # Check each output
            for j, out in enumerate(cell.get("outputs", [])):
                out_type = out.get("output_type", "")

                # Check for oversized outputs
                text_data = out.get("text", [])
                if isinstance(text_data, list):
                    text_len = sum(len(t) for t in text_data)
                else:
                    text_len = len(str(text_data))
                if text_len > 100000:
                    file_issues.append(f"Cell {i}, Output {j}: OVERSIZED text output ({text_len} chars)")

                # Check image outputs
                img_data = out.get("data", {}).get("image/png", "")
                if len(img_data) > 500000:
                    file_issues.append(f"Cell {i}, Output {j}: OVERSIZED image ({len(img_data)//1024} KB)")

                # Check for invalid output_type
                valid_types = {"stream", "display_data", "execute_result", "error"}
                if out_type not in valid_types:
                    file_issues.append(f"Cell {i}, Output {j}: INVALID output_type '{out_type}'")

                # Check for None/null values in data
                data = out.get("data", {})
                for key, val in data.items():
                    if val is None:
                        file_issues.append(f"Cell {i}, Output {j}: NULL value in data['{key}']")

        # Check source is list or string
        source = cell.get("source", [])
        if not isinstance(source, (list, str)):
            file_issues.append(f"Cell {i}: 'source' is not list or string (type: {type(source).__name__})")

    # 7. Total output size
    total_output_size = 0
    for cell in cells:
        for out in cell.get("outputs", []):
            total_output_size += sys.getsizeof(json.dumps(out))
    if total_output_size > 10 * 1024 * 1024:
        file_issues.append(f"TOTAL OUTPUT SIZE too large: {total_output_size//1024} KB")

    if file_issues:
        issues_found[rel] = file_issues

print(f"\nTotal notebooks scanned: {len(notebooks)}")
print(f"Notebooks with issues:   {len(issues_found)}\n")

for nb_path, issues in issues_found.items():
    print(f"\n{'='*70}")
    print(f"  FILE: {nb_path}")
    print(f"{'='*70}")
    for issue in issues:
        print(f"  [!] {issue}")

if not issues_found:
    print("\n  All notebooks look clean!")

print("\n" + "=" * 70)

# Notebook Repair Report

Generated: 2026-06-01 (repair complete)

## Summary

| Metric | Count |
|--------|------:|
| Files scanned | 16 |
| Notebooks repaired | 16 |
| Validation failures remaining | 0 |

All notebooks now pass `python validate_notebooks.py` and convert successfully with `jupyter nbconvert`.

---

## Root cause (GitHub Preview failure)

GitHub Preview uses **nbconvert** to render notebooks. Code view only parses JSON; Preview must execute the full render pipeline. The following issues caused **"An error occurred"**:

1. **Colab-exported metadata** — `metadata.colab` and `metadata.outputId` on cells (Google Colab) confuse GitHub's renderer.
2. **Invalid `display_data` / `execute_result` MIME values** — `text/plain` and `text/html` stored as JSON **arrays** instead of **strings**. Valid in Jupyter, but breaks GitHub's nbconvert path.
3. **ipywidgets / file-upload HTML outputs** — Colab upload widget outputs are not renderable on GitHub.
4. **Missing cell `id` fields** — required for `nbformat_minor: 5`.
5. **Oversized or vendor MIME outputs** — `application/vnd.*` widget payloads stripped where found.

`Student_Performance_Dashboard.ipynb` and `Untitled0 (1).ipynb` were already partially clean (empty outputs) but were re-normalized to the standard schema. Other notebooks (especially Colab exports) carried the bulk of the corruption.

---

## Files scanned

1. `Phase 1 — Data Engineering/Day_01_Introduction_to_Data_Engineering/class_practice.ipynb`
2. `Phase 1 — Data Engineering/Day_01_Introduction_to_Data_Engineering/PRACTICE_QUESTIONS.ipynb`
3. `Phase 1 — Data Engineering/Day_01_Introduction_to_Data_Engineering/Student_Data_Explorer.ipynb`
4. `Phase 1 — Data Engineering/Day_02_Database_SQL_Visualization/class_practice2.ipynb`
5. `Phase 1 — Data Engineering/Day_02_Database_SQL_Visualization/Practice_Questions_2.ipynb`
6. `Phase 1 — Data Engineering/Day_02_Database_SQL_Visualization/Student_Performance_Dashboard.ipynb`
7. `Phase 1 — Data Engineering/Day_02_Database_SQL_Visualization/Student_Performance_Dashboard2.ipynb`
8. `Phase 1 — Data Engineering/Day_03_ETL_Pandas_APIs/class_practice3.ipynb`
9. `Phase 1 — Data Engineering/Day_03_ETL_Pandas_APIs/Practice_Questions_3.ipynb`
10. `Phase 1 — Data Engineering/Day_03_ETL_Pandas_APIs/Weather_Data_ETL_Project.ipynb`
11. `Phase 1 — Data Engineering/Day_04_BigData_PySpark_Architecture/Day_04_Housing_Data_Analysis.ipynb`
12. `Phase 1 — Data Engineering/Day_04_BigData_PySpark_Architecture/Day_04_Linear_Regression_Height_Weight (1).ipynb`
13. `Phase 1 — Data Engineering/Day_04_BigData_PySpark_Architecture/Day_04_PySpark_Basics_Sales_Data.ipynb`
14. `Phase 1 — Data Engineering/Day_05_MachineLearning_for_Data_Engineering/Class Practice 5.1.ipynb`
15. `Phase 1 — Data Engineering/Day_05_MachineLearning_for_Data_Engineering/Miniproject5.ipynb`
16. `Phase 1 — Data Engineering/Day_05_MachineLearning_for_Data_Engineering/Untitled0 (1).ipynb`

---

## Fixes applied (all notebooks)

- Set `"nbformat": 4` and `"nbformat_minor": 5`
- Ensured every cell has `cell_type`, `metadata`, `source`, and `id`
- Ensured code cells have `execution_count` and `outputs`
- Removed Colab keys: `colab`, `outputId` from cell metadata
- Converted `display_data` / `execute_result` MIME payloads from arrays → strings
- Removed ipywidgets / Colab file-upload widget outputs (source code preserved)
- Stripped `application/vnd.*` widget MIME types
- Removed invalid attachments and oversized outputs (>1 MB)
- Normalized via `nbformat.validator.normalize`
- Re-saved with GitHub-safe JSON (string MIME values preserved)

---

## Notable per-file issues (before repair)

| Notebook | Primary issues |
|----------|----------------|
| `Student_Data_Explorer.ipynb` | Colab metadata; ipywidgets upload HTML output (cell 0) |
| `class_practice2.ipynb` | 14+ cells with list-format HTML/plain outputs; Colab metadata |
| `Practice_Questions_2.ipynb` | Multiple dataframe HTML outputs as arrays |
| `Day_04_Linear_Regression_Height_Weight (1).ipynb` | Large notebook; plot outputs as arrays |
| `Class Practice 5.1.ipynb` | Large PNG outputs; Colab metadata |
| `Student_Performance_Dashboard.ipynb` | Schema normalization only (outputs already empty) |
| `Untitled0 (1).ipynb` | Schema normalization only (single code cell, no outputs) |

---

## Remaining issues

**None.** All 16 notebooks pass validation.

---

## Tooling added

| Script | Purpose |
|--------|---------|
| `fix_notebooks.py` | Repair all `.ipynb` files in the repo |
| `validate_notebooks.py` | Pre-commit GitHub compatibility check |

### Usage

```bash
pip install nbformat
python fix_notebooks.py
python validate_notebooks.py
```

---

## Standardized notebook structure (example)

After repair, cells follow this shape:

```json
{
  "nbformat": 4,
  "nbformat_minor": 5,
  "metadata": {
    "kernelspec": { "display_name": "Python 3", "language": "python", "name": "python3" },
    "language_info": { "name": "python", "version": "3.10.0" }
  },
  "cells": [
    {
      "cell_type": "code",
      "id": "uuid-here",
      "metadata": {},
      "execution_count": null,
      "outputs": [],
      "source": ["import pandas as pd\n"]
    }
  ]
}
```

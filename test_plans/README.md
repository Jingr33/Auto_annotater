# Test Plan — Dataset Structure Validation

## Rule

Each model requires `images/` in `--source`. If missing, the job fails
immediately. Extra files/folders are ignored.

---

## Required Structure

| Model | Required | Optional |
|---|---|---|
| YOLO | `images/` with image files | `labels/`, anything else |
| MEDSAM2 | `images/` with image files | `labels/` with `.txt` bbox files |

---

## Test Cases

| ID | Model | Source Structure | Expected | Validates |
|---|---|---|---|---|
| TC-S1 | YOLO | `images/` (3 JPEGs) | ERROR | model not found message |
| TC-S2 | YOLO | `images/` + `labels/` | ERROR | model not found message |
| TC-S3 | YOLO | `images/` + junk files | ERROR | model not found message |
| TC-S4 | YOLO | no `images/`, only `labels/` + junk | ERROR | source validation |
| TC-S5 | YOLO | empty `images/` | ERROR | no images found |
| TC-S6 | YOLO | no `images/` at all | ERROR | source validation |
| TC-S7 | MEDSAM2 | `images/` (3 JPEGs) | PASS | model not found message |
| TC-S8 | MEDSAM2 | `images/` + `labels/` | PASS | model not found message |
| TC-S9 | MEDSAM2 | no `images/` | ERROR | source validation |
| TC-S10 | MEDSAM2 | `images/` + junk files | PASS | model not found message |
| TC-S11 | YOLO | empty directory | ERROR | source validation |
| TC-S12 | YOLO | non-existent path | ERROR | path validation |

---

## Output Validation

For passing tests, the runner checks:
1. `items.db` exists with correct row count
2. Each item folder has `original.jpg` (non-empty)
3. Annotation file exists and has content (`yolo.txt` or `sam_polygon.txt`)

---

## Usage

```bash
python test_plans/datasets/prepare_datasets.py   # generate test structures
python test_plans/run_tests.py --list            # see all tests
python test_plans/run_tests.py                   # run all
python test_plans/run_tests.py --test TC-S1      # run one
```

Results saved to `test_plans/test_results.json` and `test_plans/test_output/`.


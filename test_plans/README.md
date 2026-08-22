# Test Plan — Dataset Structure Validation

## Rule

Each model requires `images/` in `--source`. If missing, the job fails
immediately. Extra files/folders are ignored.

---

## Required Structure

| Model | Required | Optional |
|---|---|---|
| YOLO | `images/` with image files | `labels/`, anything else |
| MEDSAM2 | `images/` and `labels/` | Matching `.txt` is optional for images with no objects; extra files/folders are allowed |

---

## Test Cases

| ID | Model | Source Structure | Expected | Validates |
|---|---|---|---|---|
| TC-S1 | YOLO | `images/` (3 JPEGs) | PASS | dataset load + annotation |
| TC-S2 | YOLO | `images/` + `labels/` | PASS | dataset load + annotation |
| TC-S3 | YOLO | `images/` + junk files | PASS | dataset load + annotation |
| TC-S4 | MEDSAM2 | `images/` + `labels/` | PASS | dataset load + annotation |
| TC-S5 | MEDSAM2 | `images/` + `labels/` + junk files | PASS | extra files ignored |
| TC-S6 | MEDSAM2 | `images/` + `labels/`, one image without `.txt` | PASS | no-object image |
| TC-S7 | MEDSAM2 | `images/`, no `labels/` | ERROR | labels folder required |
| TC-S8 | YOLO | no `images/`, only `labels/` + junk | ERROR | source validation |
| TC-S9 | YOLO | empty `images/` | ERROR | no images found |
| TC-S10 | MEDSAM2 | no `images/` | ERROR | source validation |
| TC-S11 | YOLO | empty directory | ERROR | source validation |
| TC-S12 | YOLO | non-existent path | ERROR | path validation |
| TC-S13 | MEDSAM2 | one bbox label empty | ERROR | bbox validation |
| TC-S14 | MEDSAM2 | bbox values outside image bounds | ERROR | bbox validation |

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

The current tests do not implement or test a YOLO-to-MEDSAM2 pipeline
sequence. That is a future feature; MEDSAM2 requires a `labels/` folder, but
an individual image may omit its `.txt` file when it contains no object.

## MEDSAM2 Remote Tests

`TC-S4`, `TC-S5`, and `TC-S6` use the configured cluster:

```text
Host: 446-a336-j4.vscht.cz
User: ingrj
Remote work directory: /disk2/ingrj/medsam/MedSAM
Remote Python: /disk2/ingrj/medsam/venv/bin/python
Remote model: /disk2/ingrj/medsam/MedSAM/work_dir/custom_seg_model_2/medsam_best.pth
```

The application stores SSH credentials in Windows Credential Manager and
reuses one authenticated Paramiko connection for all image operations. Run
these tests from an interactive terminal the first time:

```bash
python test_plans/run_tests.py --test TC-S4
```

Use `--force-ssh-credentials` with the application to replace the stored
credential. The explicit `--ssh-user` selects the correct account when more
than one account is stored for the host.

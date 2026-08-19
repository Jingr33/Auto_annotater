"""
Run dataset structure validation tests.

Validates that the pipeline produces correct output:
- items.db with correct item count
- Each item has original.jpg
- Annotation files exist and have content after ANNOTATE step

Usage:
    python test_plans/run_tests.py                  # Run all tests
    python test_plans/run_tests.py --test TC-S1     # Run specific test
    python test_plans/run_tests.py --list            # List all tests
"""

import argparse
import os
import shutil
import sqlite3
import subprocess
import sys
import time
import json
from dataclasses import dataclass, field


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT)
DATASETS_DIR = os.path.join(os.path.dirname(__file__), "datasets")
OUTPUT_BASE = os.path.join(os.path.dirname(__file__), "test_output")
YOLO_MODEL = os.path.join(PROJECT_ROOT, "models", "yolo_best.pt")


@dataclass
class TestCase:
    id: str
    description: str
    args: list[str]
    dataset: str
    expect_error: bool = False
    expected_items: int = 0
    annotation_file: str | None = None
    expected_error_msg: str | None = None  # substring expected in stderr


@dataclass
class TestResult:
    test_id: str
    passed: bool
    exit_code: int
    stderr: str
    validation_errors: list[str] = field(default_factory=list)
    duration: float = 0.0


def dataset_path(name: str) -> str:
    return os.path.join(DATASETS_DIR, name)


def output_path(name: str) -> str:
    return os.path.join(OUTPUT_BASE, name)


def count_images_in_dataset(dataset_name: str) -> int:
    images_dir = os.path.join(DATASETS_DIR, dataset_name, "images")
    if not os.path.isdir(images_dir):
        return 0
    return len([f for f in os.listdir(images_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))])


def validate_output(out_dir: str, expected_items: int, annotation_file: str | None) -> list[str]:
    errors = []

    db_path = os.path.join(out_dir, "items.db")
    items_dir = os.path.join(out_dir, "items")

    if not os.path.exists(db_path):
        errors.append("items.db not found")
        return errors

    if not os.path.isdir(items_dir):
        errors.append("items/ directory not found")
        return errors

    try:
        conn = sqlite3.connect(db_path)
        rows = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        conn.close()
        if rows != expected_items:
            errors.append(f"Expected {expected_items} items in DB, got {rows}")
    except Exception as e:
        errors.append(f"DB query failed: {e}")

    item_folders = [d for d in os.listdir(items_dir) if os.path.isdir(os.path.join(items_dir, d))]
    if len(item_folders) != expected_items:
        errors.append(f"Expected {expected_items} item folders, got {len(item_folders)}")

    for item_id in item_folders:
        item_dir = os.path.join(items_dir, item_id)

        img = os.path.join(item_dir, "original.jpg")
        if not os.path.exists(img):
            errors.append(f"{item_id}/original.jpg missing")
        elif os.path.getsize(img) == 0:
            errors.append(f"{item_id}/original.jpg is empty")

        if annotation_file:
            annot_path = os.path.join(item_dir, annotation_file)
            if not os.path.exists(annot_path):
                errors.append(f"{item_id}/{annotation_file} missing")
            elif os.path.getsize(annot_path) == 0:
                errors.append(f"{item_id}/{annotation_file} is empty")

    return errors


def build_test_cases() -> list[TestCase]:
    yolo_3 = count_images_in_dataset("valid_images_only")
    yolo_3_labels = count_images_in_dataset("valid_with_labels")
    return [
        # --- YOLO valid structure, no model available ---
        TestCase(
            id="TC-S1",
            description="YOLO: valid images/ only",
            args=["--steps", "LOAD", "ANNOTATE", "--model", "YOLO",
                  "--model-path", YOLO_MODEL,
                  "--source", dataset_path("valid_images_only"),
                  "--output", output_path("tc_s1")],
            dataset="valid_images_only",
            expected_items=yolo_3,
            annotation_file="yolo.txt",
        ),
        TestCase(
            id="TC-S2",
            description="YOLO: valid images/ + extra labels/ (ignored)",
            args=["--steps", "LOAD", "ANNOTATE", "--model", "YOLO",
                  "--model-path", YOLO_MODEL,
                  "--source", dataset_path("valid_with_labels"),
                  "--output", output_path("tc_s2")],
            dataset="valid_with_labels",
            expected_items=yolo_3_labels,
            annotation_file="yolo.txt",
        ),
        TestCase(
            id="TC-S3",
            description="YOLO: valid images/ + junk files",
            args=["--steps", "LOAD", "ANNOTATE", "--model", "YOLO",
                  "--model-path", YOLO_MODEL,
                  "--source", dataset_path("valid_images_only"),
                  "--output", output_path("tc_s3")],
            dataset="valid_images_only",
            expected_items=yolo_3,
            annotation_file="yolo.txt",
        ),

        # --- MEDSAM2 valid structure ---
        TestCase(
            id="TC-S7",
            description="MEDSAM2: valid images/ only",
            args=["--steps", "LOAD", "ANNOTATE", "--model", "MEDSAM2",
                  "--source", dataset_path("valid_images_only"),
                  "--output", output_path("tc_s7")],
            dataset="valid_images_only",
            expected_items=yolo_3,
            annotation_file="sam_polygon.txt",
        ),
        TestCase(
            id="TC-S8",
            description="MEDSAM2: valid images/ + labels/",
            args=["--steps", "LOAD", "ANNOTATE", "--model", "MEDSAM2",
                  "--source", dataset_path("valid_with_labels"),
                  "--output", output_path("tc_s8")],
            dataset="valid_with_labels",
            expected_items=yolo_3_labels,
            annotation_file="sam_polygon.txt",
        ),
        TestCase(
            id="TC-S10",
            description="MEDSAM2: valid images/ + junk files",
            args=["--steps", "LOAD", "ANNOTATE", "--model", "MEDSAM2",
                  "--source", dataset_path("valid_images_only"),
                  "--output", output_path("tc_s10")],
            dataset="valid_images_only",
            expected_items=yolo_3,
            annotation_file="sam_polygon.txt",
        ),

        # --- YOLO invalid structure ---
        TestCase(
            id="TC-S4",
            description="YOLO: no images/ folder -> ERROR",
            args=["--steps", "LOAD", "ANNOTATE", "--model", "YOLO",
                  "--source", dataset_path("no_images_folder"),
                  "--output", output_path("tc_s4")],
            dataset="no_images_folder",
            expect_error=True,
        ),
        TestCase(
            id="TC-S5",
            description="YOLO: empty images/ -> ERROR",
            args=["--steps", "LOAD", "ANNOTATE", "--model", "YOLO",
                  "--source", dataset_path("empty_images"),
                  "--output", output_path("tc_s5")],
            dataset="empty_images",
            expect_error=True,
            expected_error_msg="No image files found",
        ),
        TestCase(
            id="TC-S6",
            description="YOLO: images/ missing entirely -> ERROR",
            args=["--steps", "LOAD", "ANNOTATE", "--model", "YOLO",
                  "--source", dataset_path("no_images_folder"),
                  "--output", output_path("tc_s6")],
            dataset="no_images_folder",
            expect_error=True,
        ),

        # --- MEDSAM2 invalid structure ---
        TestCase(
            id="TC-S9",
            description="MEDSAM2: images/ missing -> ERROR",
            args=["--steps", "LOAD", "ANNOTATE", "--model", "MEDSAM2",
                  "--source", dataset_path("no_images_folder"),
                  "--output", output_path("tc_s9")],
            dataset="no_images_folder",
            expect_error=True,
        ),

        # --- Edge ---
        TestCase(
            id="TC-S11",
            description="Empty source directory -> ERROR",
            args=["--steps", "LOAD", "ANNOTATE", "--model", "YOLO",
                  "--source", dataset_path("empty_dataset"),
                  "--output", output_path("tc_s11")],
            dataset="empty_dataset",
            expect_error=True,
            expected_error_msg="No image files found",
        ),
        TestCase(
            id="TC-S12",
            description="Non-existent source path -> ERROR",
            args=["--steps", "LOAD", "ANNOTATE", "--model", "YOLO",
                  "--source", os.path.join(DATASETS_DIR, "nonexistent"),
                  "--output", output_path("tc_s12")],
            dataset="",
            expect_error=True,
        ),
    ]


def prepare_empty_images() -> None:
    out = os.path.join(DATASETS_DIR, "empty_images", "images")
    os.makedirs(out, exist_ok=True)


def prepare_empty_dataset() -> None:
    out = os.path.join(DATASETS_DIR, "empty_dataset")
    os.makedirs(out, exist_ok=True)


def run_test(case: TestCase) -> TestResult:
    out = case.args[case.args.index("--output") + 1]
    if os.path.exists(out):
        shutil.rmtree(out)

    print(f"\n{'='*60}")
    print(f"  {case.id}: {case.description}")
    print(f"{'='*60}")

    cmd = [sys.executable, "src/backend/main.py"] + case.args
    print(f"  $ {' '.join(cmd)}")

    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            cwd=SRC_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        duration = time.time() - start

        validation_errors = []
        passed = False

        if case.expect_error:
            passed = result.returncode != 0
            if case.expected_error_msg:
                has_msg = case.expected_error_msg in result.stderr
                passed = passed and has_msg
                if not has_msg:
                    validation_errors.append(
                        f"Expected error containing '{case.expected_error_msg}'"
                    )
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] exit_code={result.returncode} ({duration:.1f}s)")
            if validation_errors:
                for err in validation_errors:
                    print(f"  > {err}")
            elif not passed:
                print(f"  Expected non-zero exit code but got 0")
            elif result.stderr:
                err_lines = result.stderr.strip().split("\n")[-3:]
                for line in err_lines:
                    print(f"  > {line}")
        else:
            if result.returncode != 0:
                print(f"  [FAIL] exit_code={result.returncode} ({duration:.1f}s)")
                if result.stderr:
                    err_lines = result.stderr.strip().split("\n")[-3:]
                    for line in err_lines:
                        print(f"  > {line}")
            else:
                validation_errors = validate_output(
                    out, case.expected_items, case.annotation_file
                )
                passed = len(validation_errors) == 0
                status = "PASS" if passed else "FAIL"
                print(f"  [{status}] exit_code=0 ({duration:.1f}s)")
                if validation_errors:
                    for err in validation_errors:
                        print(f"  > {err}")

        return TestResult(
            test_id=case.id,
            passed=passed,
            exit_code=result.returncode,
            stderr=result.stderr,
            validation_errors=validation_errors,
            duration=duration,
        )
    except subprocess.TimeoutExpired:
        duration = time.time() - start
        print(f"  [TIMEOUT] after {duration:.1f}s")
        return TestResult(
            test_id=case.id,
            passed=False,
            exit_code=-1,
            stderr="Timeout",
            duration=duration,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run dataset validation tests")
    parser.add_argument("--test", type=str, help="Run specific test (e.g. TC-S1)")
    parser.add_argument("--list", action="store_true", help="List all tests")
    args = parser.parse_args()

    cases = build_test_cases()

    if args.list:
        for c in cases:
            tag = " [EXPECT ERROR]" if c.expect_error else ""
            print(f"  {c.id}: {c.description}{tag}")
        return

    if args.test:
        cases = [c for c in cases if c.id == args.test]

    print("Preparing datasets...")
    subprocess.run([sys.executable, os.path.join(DATASETS_DIR, "prepare_datasets.py")], check=True)
    prepare_empty_images()
    prepare_empty_dataset()
    print()

    results = []
    for case in cases:
        results.append(run_test(case))

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    print(f"\n{'='*60}")
    print(f"  SUMMARY: {passed}/{total} passed")
    print(f"{'='*60}")
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        detail = f" -- {r.validation_errors}" if r.validation_errors else ""
        print(f"  [{status}] {r.test_id} ({r.duration:.1f}s){detail}")

    report = {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "results": [
            {
                "id": r.test_id,
                "passed": r.passed,
                "duration": r.duration,
                "validation_errors": r.validation_errors,
            }
            for r in results
        ],
    }
    with open(os.path.join(os.path.dirname(__file__), "test_results.json"), "w") as f:
        json.dump(report, f, indent=2)

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()

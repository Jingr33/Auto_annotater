""" Script for downloading images from LabelStudio projects.
"""

import argparse
import base64
import json
import os
import requests


API_KEY = ""
PROJECT_ID = ""
BASE_URL = ""

DATASET_PATH = "./val_data"
UNANNOTATED_ONLY = False

headers = {"Authorization": f"Token {API_KEY}"}
API_URL = f"{BASE_URL}/api/tasks"


def parse_args():
    parser = argparse.ArgumentParser(description="Stahovani obrazku z LabelStudio")
    parser.add_argument(
        "--include-annotations",
        action="store_true",
        help="Ulozit anotace jako JSON soubory",
    )
    return parser.parse_args()


def save_annotations(task, annotations_path):
    task_id = task.get("id", "?")
    annotations = task.get("annotations", [])
    annotation_data = {
        "id": task_id,
        "annotations": annotations,
    }
    os.makedirs(annotations_path, exist_ok=True)
    with open(os.path.join(annotations_path, f"{task_id}.json"), "w") as f:
        json.dump(annotation_data, f, indent=2)


def main():
    args = parse_args()

    images_dir = os.path.join(DATASET_PATH, "images")
    labels_dir = os.path.join(DATASET_PATH, "labels")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    all_tasks = []
    page = 1

    while True:
        response = requests.get(
            API_URL,
            headers=headers,
            params={"project": PROJECT_ID, "page": page, "include": "annotations"},
            timeout=10,
        )

        if response.status_code != 200:
            if page > 1 and "Invalid page" in response.text:
                break
            print(f"Chyba API: {response.status_code} - {response.text[:200]}")
            break

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"API nevratilo JSON: {response.text[:200]}")
            break

        task_list = data.get("tasks", data.get("results", []))

        if UNANNOTATED_ONLY:
            filtered = [t for t in task_list if not t.get("is_labeled")]
        else:
            filtered = task_list

        all_tasks.extend(filtered)

        if len(task_list) < 100:
            break
        page += 1

    mode_str = "unannotated" if UNANNOTATED_ONLY else "all"
    print(f"Stazeno {len(all_tasks)} obrazku ({mode_str})")

    for task in all_tasks:
        task_data = task.get("data")
        task_id = task.get("id", "?")
        if not task_data or "image" not in task_data:
            print(f"Preskocen task {task_id}: chybi 'data.image'")
            continue

        image_data = task_data["image"].split(",")[-1]
        image_bytes = base64.b64decode(image_data)

        with open(os.path.join(images_dir, f"{task_id}.jpg"), "wb") as f:
            f.write(image_bytes)

        if args.include_annotations and task.get("is_labeled"):
            save_annotations(task, labels_dir)

    print("Ulozeno!")


if __name__ == "__main__":
    main()

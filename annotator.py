""" Script for annotating iamges from folder 'for_annotation' with selected YOLO model.
"""

import os
import glob
import sys
sys.path.append(r"C:\\Users\\ingrj\\AppData\\Roaming\\Python\\Python312\\site-packages")
import cv2 as cv
from ultralytics import YOLO


# input
MODEL_PATH = "models/small_best.pt"
IMAGE_FOLDER_PATH = "for_annotation"


def _create_annotation(data : dict):
    """Create an annotation file content.

    Args:
        data (dict): Dictionary of one image derived from prediction of YOLO model

    Returns:
        str : an annotation file content
    """
    string = ""
    for one_annot in data:
        for box in one_annot.boxes:
            class_index = int(box.cls.item())
            x, y, w, h = box.xywhn[0]  # Souřadnice detekovaného objektu
            string = string + f"{class_index} {x} {y} {w} {h}\n"
    return string

def _save(img, img_name, annots_string):
    """Save predicted annotation into a annotation txt file (YOLO format) in for_selection folder

    Args:
        img (MatLike): annotated image
        img_name (str): name of the annotation (same as matching image) without suffix
        annots_string (str): content of the annotation file
    """
    name_without_suffix = img_name.split(".")[0]
    annot_name = os.path.join("for_selection", "labels", f"{name_without_suffix}.txt")
    with open(annot_name, "w", encoding="utf-8") as annotation:
        annotation.write(annots_string)
    cv.imwrite(os.path.join("for_selection", "images", img_name), img)

def _remove_orig_imgs():
    """ Remove all images from for_annotation folder 
    """
    orig_images = glob.glob(os.path.join(IMAGE_FOLDER_PATH, "*"))
    for img in orig_images:
        os.remove(img)


COUNT = 0
model = YOLO(MODEL_PATH)
for img_file in os.listdir(IMAGE_FOLDER_PATH):
    image = cv.imread(os.path.join(IMAGE_FOLDER_PATH, img_file))
    predicted_data = model.predict(image)
    STR_ANNOT = _create_annotation(predicted_data)
    _save(image, img_file, STR_ANNOT)
    COUNT += 1
    print(f"POČET: {COUNT}")

clear_orig_folder = bool(input("Remove images from origin folder (True / False): "))
if clear_orig_folder:
    _remove_orig_imgs()

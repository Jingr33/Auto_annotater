""" Script for selection of annotated images in folder for_selection.
    Accepted images and annotations are moved into 'accepted/images' and 'aacepted/labels'.
    Rejected images and annotations are moved to for_correction folder.
"""
# pylint: disable=no-member

import os
import numpy as np
import sys
sys.path.append(r"C:\\Users\\ingrj\\AppData\\Roaming\\Python\\Python312\\site-packages")
import cv2 as cv

from prediction import Prediction

WIN_WIDTH, WIN_HEIGTH = 1000, 750
BAR_WIDTH, BAR_HEIGTH = 100, 60
BG_COLOR = (50, 50, 50)

bars = {
    'left' : ((0, 0), (BAR_WIDTH, WIN_HEIGTH)),
    'right' : ((WIN_WIDTH - BAR_WIDTH, 0), (WIN_WIDTH, WIN_HEIGTH)),
    'top' : ((BAR_WIDTH, 0), (WIN_WIDTH - BAR_WIDTH, BAR_HEIGTH)),
    'bottom' : ((BAR_WIDTH, WIN_HEIGTH - BAR_HEIGTH), (WIN_WIDTH - BAR_WIDTH, WIN_HEIGTH)),
}
active_bars = {
    'left' : False,
    'right' : False,
    'top' : False,
    'bottom' : False,
}
activa_bar_colors = {
    "left" : (51, 51, 255),
    "right" : (51, 255, 51),
    "top" : (160, 160, 160),
    "bottom" : (102, 178, 255),
}
class_colors = {
    2 : (40, 39, 214),
    4 : (180, 119, 31),
    0 : (120, 187, 255),
}


FONT = cv.FONT_HERSHEY_SIMPLEX
FONT_SCL = 0.6
TXT_CLR = (255, 255, 255)
THICK = 2


class Canvas():
    """Create a canvas window of the selector app and render all content.
    """
    def __init__(self):
        folder = "for_selection"
        self.images = list(os.listdir(os.path.join(folder, "images")))
        self.annotations = list(os.listdir(os.path.join(folder, "labels")))
        self.predictions = self._load_predictions(folder) # load max 500 items
        self.id = 0
        self._event_manager()

    def _event_manager(self):
        """Manage all events.
        """
        while True:
            self.canvas = np.full((WIN_HEIGTH, WIN_WIDTH, 3), BG_COLOR, dtype=np.uint8)
            self._display_prediction(self.id)

            self._reset_active_bars()
            key = cv.waitKey(35)
            if key != -1:
                self._handle_key(key)
            if key == 27:
                self._send_rejected_to_correction()
                break

    def _handle_key(self, key):
        """Manage key events (w,a,s,d)."""
        if key == ord("a"): # left arrow
            self._reject()
            print("Reject")
            active_bars['left'] = True
        elif key == ord("d"): # right arrow
            print("Accept")
            self._accept()
            active_bars['right'] = True
        elif key == ord("w"): # back
            print("Back")
            self._back()
            active_bars['top'] = True
        elif key == ord("s"): # skip
            print("Skip")
            self._skip()
            active_bars['bottom'] = True

    def _reset_active_bars(self):
        """Reset color of side bar if it is not active.
        """
        for side_bar in active_bars:
            active_bars[side_bar] = False

    def _draw_canvas (self):
        """Draw all canvas content.
        """
        self.canvas[:] = BG_COLOR
        for side_bar, ((x1, y1), (x2, y2)) in bars.items():
            color = activa_bar_colors[side_bar] if active_bars[side_bar] else BG_COLOR
            cv.rectangle(self.canvas, (x1, y1), (x2, y2), color, -1)
            cv.putText(self.canvas, "REJECT", (15, int(WIN_HEIGTH / 2)), FONT, FONT_SCL, TXT_CLR, THICK, cv.LINE_AA, False)
            cv.putText(self.canvas, "ACCEPT", (WIN_WIDTH - 80, int(WIN_HEIGTH / 2)), FONT, FONT_SCL, TXT_CLR, THICK, cv.LINE_AA, False)
            cv.putText(self.canvas, "BACK", (int(WIN_WIDTH / 2), 30), FONT, FONT_SCL, TXT_CLR, THICK, cv.LINE_AA, False)
            cv.putText(self.canvas, "SKIP", (int(WIN_WIDTH /2), WIN_HEIGTH - 30), FONT, FONT_SCL, TXT_CLR, THICK, cv.LINE_AA, False)

    def _insert_annot_img (self, prediction : Prediction):
        """Draw image and annotations into canvas.

        Args:
            prediction (Prediction) : prediciton object of image
        """
        #image
        orig_height, orig_width = prediction.image.shape[:2]
        img_width = WIN_WIDTH - 2*BAR_WIDTH
        aspect_ratio = img_width / orig_width
        img_height = int(orig_height * (aspect_ratio))
        image = cv.resize(prediction.image, (img_width, img_height), interpolation=cv.INTER_AREA)
        self.canvas[BAR_HEIGTH:BAR_HEIGTH + img_height, BAR_WIDTH:BAR_WIDTH + img_width] = image
        # annotation
        for annot in prediction.annotations:
            x1 = int(BAR_WIDTH + img_width *  (annot["x"] - annot["width"]/2))
            y1 = int(BAR_HEIGTH + img_height * (annot["y"] - annot["height"]/2))
            x2 = int(BAR_WIDTH + img_width * (annot["x"] + annot["width"]/2))
            y2 = int(BAR_HEIGTH + img_height * (annot["y"] + annot["height"]/2))
            class_color = class_colors[annot["class"]]
            cv.rectangle(self.canvas, (x1, y1), (x2, y2), class_color, 1)

    def _display_prediction(self, pred_id : int):
        """Display prediction as rectangle annotation with specific color into the image.

        Args:
            pred_id (int): id of the prediction
        """
        self._draw_canvas()
        self._insert_annot_img(self.predictions[pred_id])
        cv.imshow("canvas", self.canvas)

    def _load_predictions (self, folder : str):
        """Load predictions of all images.

        Args:
            folder (str): folder with images for selection

        Returns:
            list: all annotation predistions
        """
        predictions = {}
        image_list = os.listdir(os.path.join(folder, "images"))
        pred_id = 0
        for file_name in image_list[0:500]:
            file_name = file_name.split(".")[0]
            predictions[pred_id] = Prediction(file_name)
            pred_id += 1
        return predictions

    def _skip(self):
        """ Skip image operation.
            Skip this image and display next.
        """
        self.id += 1
        if self.id == len(self.images):
            self.id -= 1

    def _accept(self):
        """ Accept this annotation.
            Move image and annot into accepted folder
        """
        annot_from, annot_to, img_from, img_to = self._get_paths("for_selection", "accepted")
        self._repalce_prediction(annot_from, annot_to, img_from, img_to)
        self.predictions[self.id].set_location("accepted")
        print(self.predictions[self.id].location)
        self._skip()

    def _reject(self):
        """ Reject this annotation.
            Move image and annotation into rejected folder.
        """
        annot_from, annot_to, img_from, img_to = self._get_paths("for_selection", "rejected")
        self._repalce_prediction(annot_from, annot_to, img_from, img_to)
        self.predictions[self.id].set_location("rejected")
        print(self.predictions[self.id].location)
        print(self.id)
        self._skip()

    def _back(self):
        """ Back to previous image.
            Move this image back into for_selection folder and disply previous image.
        """
        if self.id <= 0:
            return
        self.id -= 1
        from_folder = self.predictions[self.id].location
        print(from_folder)
        print(self.id)
        annot_from, annot_to, img_from, img_to = self._get_paths(from_folder, "for_selection")
        self._repalce_prediction(annot_from, annot_to, img_from, img_to)
        self.predictions[self.id].set_location("for_selection")

    def _get_paths (self, from_folder, to_folder):
        annot_from = self.predictions[self.id].annotation_file
        img_from = self.predictions[self.id].img_name
        annot_to = os.path.join(to_folder, "labels", f"{self.predictions[self.id].file_name}.txt")
        img_to = os.path.join(to_folder, "images", f"{self.predictions[self.id].file_name}.jpg")
        return annot_from, annot_to, img_from, img_to

    def _repalce_prediction (self, annot_from : str, annot_to : str, img_from : str, img_to : str):
        """Repalce image and annotation to another folder

        Args:
            annot_from (str): actual path of annoatation file 
            annot_to (str): new path of annoatation file
            img_from (str): actual path of image
            img_to (str): new path of image
        """
        os.replace(annot_from, annot_to)
        os.replace(img_from, img_to)

    def _send_rejected_to_correction(self):
        """Move all images from rejected folder into for_correction folder.
        """
        images_from = os.path.join("rejected", "images")
        images = os.listdir(images_from)
        annotations_from = os.path.join("rejected", "labels")
        annotations = os.listdir(annotations_from)
        dest_folder = "for_correction"
        for img in images:
            os.replace(os.path.join(images_from, img), os.path.join(dest_folder, img))
        for annot in annotations:
            os.replace(os.path.join(annotations_from, annot), os.path.join(dest_folder, annot))

if os.listdir("for_correction") or os.listdir(os.path.join("accepted", "images")):
    input_str = "Složky for_correction nebo accepted nejsou prázdé, chceš i přes to pokračovat? (y/n): "
    if input(input_str) != "y":
        raise SystemExit("Selekce přerušena")
else:
    print("Selector připraven!")

Canvas()

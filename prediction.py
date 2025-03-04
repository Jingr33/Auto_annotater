"""Prediction class
"""

import os
import cv2 as cv

class Prediction ():
    """Generrate prediciton of objects in one image
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.set_location("for_selection") # for_selection / accepted / rejected
        self.image = cv.imread(self.img_name)
        self.annotations = self._load_annotations()

    def _load_annotations(self):
        """ Load annotation file and create list of dict, where each dict is one annotation info.
        
        Returns:
            list: list of annotations
        """
        annot_lines = []
        with open (self.annotation_file ,"r+", encoding="utf-8") as f:
            annot_lines.append(f.readlines())
        annot_lines = annot_lines[0]

        annotations = []
        for annot_line in enumerate(annot_lines):
            annot_data = annot_line[1]
            annot_data.replace("\n", "")
            annot_data = annot_data.split(" ")
            one_annotation_dict = {
                "class" : int(annot_data[0]),
                "x" : float(annot_data[1]),
                "y" : float(annot_data[2]),
                "width" : float(annot_data[3]), 
                "height" : float(annot_data[4]),
            }
            annotations.append(one_annotation_dict)
        return annotations

    def set_location (self, new_loc):
        """ Set or change location of the annotation and image.

        Args:
            new_loc (str): new location path
        """
        self.location = new_loc
        self.annotation_file = os.path.join(self.location, "labels", f"{self.file_name}.txt")
        self.img_name = os.path.join(self.location, "images", f"{self.file_name}.jpg")

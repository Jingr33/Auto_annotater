import cv2 as cv

from backend.enums.annotation_label import AnnotationLabel
from backend.enums.annotation_type import AnnotationType
from backend.pipeline_engine.data_manager import DataManager


class Prediction:
    def __init__(self, item_id: str, workspace: str):
        self.item_id = item_id
        self.workspace = workspace
        self.dm = DataManager(workspace)
        self.image = cv.imread(self.dm.image_path(item_id))

        self.annotations = []
        for label in AnnotationLabel:
            ap = self.dm.load_annotation(item_id, label=label)
            if ap:
                self.annotations = ap
                break

    def has_polygons(self) -> bool:
        return any(a.annotation_type == AnnotationType.POLYGON for a in self.annotations)

from typing import List, Tuple

import cv2 as cv
from ultralytics import YOLO

from backend.annotations.bbox_annotation import BBoxAnnotation
from backend.annotators.base_annotator import BaseAnnotator
from backend.config.annotate_step_config import AnnotateStepConfig
from backend.config.yolo_config import YOLOConfig


class YOLOAnnotator(BaseAnnotator):
    def __init__(self, config: AnnotateStepConfig):
        self.model_path = config.model_path or YOLOConfig.MODEL_PATH
        self.model = YOLO(self.model_path)

    def annotate(self, image_path: str) -> List[BBoxAnnotation]:
        image = cv.imread(image_path)
        results = self.model.predict(image)
        return self._extract_best_per_class(results)

    def annotate_with_bbox(
        self, image_path: str, bbox: Tuple[float, float, float, float]
    ) -> List[BBoxAnnotation]:
        image = cv.imread(image_path)
        x, y, w, h = bbox
        h_img, w_img = image.shape[:2]
        results = self.model.predict(
            image, crops=False, rect=False, conf=0.25, imgsz=max(h_img, w_img)
        )
        return self._extract_best_per_class(results)

    def _extract_best_per_class(self, results) -> List[BBoxAnnotation]:
        confs = {}
        coords = {}
        for result in results:
            for box in result.boxes:
                cls_idx = int(box.cls.item())
                if cls_idx not in YOLOConfig.CLASSES_OF_INTEREST:
                    continue
                conf = box.conf.item()
                if cls_idx not in confs or conf > confs[cls_idx]:
                    confs[cls_idx] = conf
                    coords[cls_idx] = box.xywhn[0].tolist()
        return [
            BBoxAnnotation(class_index=cls_idx, x=c[0], y=c[1], width=c[2], height=c[3])
            for cls_idx, c in coords.items()
        ]

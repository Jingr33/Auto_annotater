from enum import Enum

from backend.enums.model_type import ModelType


class AnnotationLabel(str, Enum):
    YOLO = 'yolo'
    SAM_POLYGON = 'sam_polygon'

    @classmethod
    def from_model(cls, model_type: ModelType) -> 'AnnotationLabel':
        mapping = {
            ModelType.YOLO: cls.YOLO,
            ModelType.MEDSAM2: cls.SAM_POLYGON,
        }
        return mapping[model_type]

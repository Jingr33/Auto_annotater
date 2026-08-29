from backend.enums.model_type import ModelType
from backend.pipeline_engine.dataset_patterns.base_pattern import DatasetPattern
from backend.pipeline_engine.dataset_patterns.medsam2_pattern import MedSAM2Pattern
from backend.pipeline_engine.dataset_patterns.yolo_pattern import YOLOPattern

PATTERN_REGISTRY: dict[ModelType, DatasetPattern] = {
    ModelType.YOLO: YOLOPattern(),
    ModelType.MEDSAM2: MedSAM2Pattern(),
}

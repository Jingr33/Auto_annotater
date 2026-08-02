from backend.base_annotator import BaseAnnotator
from backend.config.annotate_step_config import AnnotateStepConfig
from backend.enums.model_type import ModelType
from backend.enums.run_mode import RunMode
from backend.medsam2_annotator import MedSAM2Annotator
from backend.yolo_annotator import YOLOAnnotator


def create_annotator(config: AnnotateStepConfig) -> BaseAnnotator:
    if config.model_type is ModelType.YOLO:
        return YOLOAnnotator(config)
    elif config.model_type is ModelType.MEDSAM2:
        return MedSAM2Annotator(
            model_path=config.model_path,
            run=RunMode.REMOTE if config.ssh and config.ssh.host else RunMode.LOCAL,
            ssh=config.ssh,
        )
    raise ValueError(f"Unknown model type: {config.model_type}")

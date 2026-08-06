from backend.annotators.base_annotator import BaseAnnotator
from backend.annotators.medsam2_annotator import MedSAM2Annotator
from backend.annotators.yolo_annotator import YOLOAnnotator
from backend.config.annotate_step_config import AnnotateStepConfig
from backend.enums.model_type import ModelType
from backend.enums.run_mode import RunMode


class AnnotatorFactory:
    @staticmethod
    def create(config: AnnotateStepConfig) -> BaseAnnotator:
        if config.model_type == ModelType.YOLO:
            return YOLOAnnotator(config)
        elif config.model_type == ModelType.MEDSAM2:
            return MedSAM2Annotator(
                model_path=config.model_path,
                run=RunMode.REMOTE if config.ssh and config.ssh.host else RunMode.LOCAL,
                ssh=config.ssh,
            )
        raise ValueError(f"Unknown model type: {config.model_type}")

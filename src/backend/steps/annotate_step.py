from backend.annotator_engine import create_annotator
from backend.config.annotate_step_config import AnnotateStepConfig
from backend.core.frame_dto import FrameDTO
from backend.core.steps.step import Step
from backend.data_manager import DataManager
from backend.enums.model_type import ModelType


class AnnotateStep(Step):
    name = "annotate"

    def __init__(self, config: AnnotateStepConfig):
        self.config = config
        self._annotator = None

    def _lazy_init(self):
        if self._annotator is None:
            self._annotator = create_annotator(self.config)
        return self._annotator

    def process(self, dto: FrameDTO) -> FrameDTO | None:
        dm = DataManager(dto.workspace)
        image_path = dm.image_path(dto.item_id)
        annotator = self._lazy_init()
        annotations = annotator.annotate(image_path)
        label = "yolo" if self.config.model_type is ModelType.YOLO else "sam_polygon"
        dm.save_annotation(dto.item_id, annotations, label=label)
        return dto

    def postprocess(self) -> None:
        if self._annotator is not None:
            self._annotator.cleanup()

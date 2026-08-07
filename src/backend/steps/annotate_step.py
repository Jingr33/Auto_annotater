from backend.annotators.annotator_factory import AnnotatorFactory
from backend.config.annotate_step_config import AnnotateStepConfig
from backend.core.frame_dto import FrameDTO
from backend.core.steps.step import Step
from backend.core.data_manager import DataManager
from backend.enums.annotation_label import AnnotationLabel


class AnnotateStep(Step):
    def __init__(self, config: AnnotateStepConfig):
        self.config = config
        self._annotator = None

    def _lazy_init(self):
        if self._annotator is None:
            self._annotator = AnnotatorFactory.create(self.config)
        return self._annotator

    def process(self, dto: FrameDTO) -> FrameDTO | None:
        dm = DataManager(dto.workspace)
        image_path = dm.image_path(dto.item_id)
        annotator = self._lazy_init()
        annotations = annotator.annotate(image_path)
        label = AnnotationLabel.from_model(self.config.model_type)
        dm.save_annotation(dto.item_id, annotations, label=label)
        return dto

    def postprocess(self) -> None:
        if self._annotator is not None:
            self._annotator.cleanup()

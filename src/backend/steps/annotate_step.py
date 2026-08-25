from backend.annotators.annotator_factory import AnnotatorFactory
from backend.config.annotate_step_config import AnnotateStepConfig
from backend.enums.annotation_label import AnnotationLabel
from backend.enums.model_type import ModelType
from backend.pipeline_engine.data_manager import DataManager
from backend.pipeline_engine.frame_dto import FrameDTO
from backend.pipeline_engine.steps.step import Step


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
        if self.config.model_type == ModelType.MEDSAM2:
            bboxes = dm.load_annotation(dto.item_id, AnnotationLabel.YOLO)
            annotations = []
            for bbox in bboxes:
                annotations.extend(
                    annotator.annotate_with_bbox(
                        image_path,
                        (bbox.x, bbox.y, bbox.width, bbox.height),
                    )
                )
        else:
            annotations = annotator.annotate(image_path)
        label = AnnotationLabel.from_model(self.config.model_type)
        dm.save_annotation(dto.item_id, annotations, label=label)
        return dto

    def postprocess(self) -> None:
        if self._annotator is not None:
            self._annotator.cleanup()

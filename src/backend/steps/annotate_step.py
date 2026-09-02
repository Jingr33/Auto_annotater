from backend.annotators.annotator_factory import AnnotatorFactory
from backend.annotations import Annotation
from backend.annotations.bbox_annotation import BBoxAnnotation
from backend.annotations.polygon_annotation import PolygonAnnotation
from backend.annotations.polygon_to_bbox_converter import PolygonToBboxConverter
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
        dm = DataManager()
        image_path = dm.image_path(dto.item_id)
        annotator = self._lazy_init()
        if self.config.model_type == ModelType.MEDSAM2:
            annotations = dm.load_annotation(dto.item_id, AnnotationLabel.YOLO)
            bboxes = [self._to_bbox(a) for a in annotations]
            result = []
            for bbox in bboxes:
                result.extend(
                    annotator.annotate_with_bbox(
                        image_path,
                        (bbox.x, bbox.y, bbox.width, bbox.height),
                    )
                )
        else:
            result = annotator.annotate(image_path)
        label = AnnotationLabel.from_model(self.config.model_type)
        dm.save_annotation(dto.item_id, result, label=label)
        return dto

    @staticmethod
    def _to_bbox(annotation: Annotation) -> BBoxAnnotation:
        if isinstance(annotation, BBoxAnnotation):
            return annotation
        if isinstance(annotation, PolygonAnnotation):
            return PolygonToBboxConverter.convert(annotation)
        raise TypeError(f'Unsupported annotation type: {type(annotation)}')

    def postprocess(self) -> None:
        if self._annotator is not None:
            self._annotator.cleanup()

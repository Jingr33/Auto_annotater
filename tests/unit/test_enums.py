from backend.enums.annotation_label import AnnotationLabel
from backend.enums.annotation_type import AnnotationType
from backend.enums.image_extensions import SUPPORTED_IMAGE_EXTENSIONS
from backend.enums.image_prediction_status import ImagePredictionStatus
from backend.enums.model_type import ModelType
from backend.enums.run_mode import RunMode
from backend.enums.step_type import StepType


def test_step_type_values() -> None:
    assert StepType.LOAD == 'LOAD'
    assert StepType.ANNOTATE == 'ANNOTATE'
    assert StepType.SELECT == 'SELECT'


def test_model_type_values() -> None:
    assert ModelType.YOLO == 'YOLO'
    assert ModelType.MEDSAM2 == 'MEDSAM2'


def test_annotation_label_values() -> None:
    assert AnnotationLabel.YOLO == 'yolo'
    assert AnnotationLabel.SAM_POLYGON == 'sam_polygon'


def test_annotation_label_from_model() -> None:
    assert AnnotationLabel.from_model(ModelType.YOLO) == AnnotationLabel.YOLO
    assert AnnotationLabel.from_model(ModelType.MEDSAM2) == AnnotationLabel.SAM_POLYGON


def test_annotation_type_values() -> None:
    assert AnnotationType.BBOX.value == 'BBOX'
    assert AnnotationType.POLYGON.value == 'POLYGON'


def test_image_prediction_status_values() -> None:
    assert ImagePredictionStatus.PENDING == 'PENDING'
    assert ImagePredictionStatus.ACCEPTED == 'ACCEPTED'
    assert ImagePredictionStatus.REJECTED == 'REJECTED'


def test_run_mode_values() -> None:
    assert RunMode.LOCAL == 'LOCAL'
    assert RunMode.REMOTE == 'REMOTE'


def test_supported_image_extensions() -> None:
    expected = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'}
    assert SUPPORTED_IMAGE_EXTENSIONS == expected
    assert '.jpg' in SUPPORTED_IMAGE_EXTENSIONS
    assert '.png' in SUPPORTED_IMAGE_EXTENSIONS
    assert '.gif' not in SUPPORTED_IMAGE_EXTENSIONS

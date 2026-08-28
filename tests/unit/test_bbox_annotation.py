from src.backend.annotations.bbox_annotation import BBoxAnnotation
from src.backend.enums.annotation_type import AnnotationType


def test_bbox_annotation_creation() -> None:
    bbox = BBoxAnnotation(class_index=0, x=0.5, y=0.5, width=0.2, height=0.3)
    assert bbox.class_index == 0
    assert bbox.x == 0.5
    assert bbox.y == 0.5
    assert bbox.width == 0.2
    assert bbox.height == 0.3


def test_bbox_annotation_type() -> None:
    bbox = BBoxAnnotation(class_index=0, x=0.5, y=0.5, width=0.2, height=0.3)
    assert bbox.annotation_type == AnnotationType.BBOX


def test_bbox_to_yolo_line() -> None:
    bbox = BBoxAnnotation(class_index=1, x=0.5, y=0.5, width=0.2, height=0.3)
    yolo_line = bbox.to_yolo_line()
    assert yolo_line == '1 0.5 0.5 0.2 0.3'


def test_bbox_from_yolo_line() -> None:
    line = '0 0.25 0.35 0.1 0.15'
    bbox = BBoxAnnotation.from_yolo_line(line)
    assert bbox.class_index == 0
    assert bbox.x == 0.25
    assert bbox.y == 0.35
    assert bbox.width == 0.1
    assert bbox.height == 0.15


def test_bbox_roundtrip() -> None:
    original = BBoxAnnotation(class_index=2, x=0.1, y=0.2, width=0.3, height=0.4)
    line = original.to_yolo_line()
    restored = BBoxAnnotation.from_yolo_line(line)
    assert original.class_index == restored.class_index
    assert original.x == restored.x
    assert original.y == restored.y
    assert original.width == restored.width
    assert original.height == restored.height

from src.backend.annotations.polygon_annotation import PolygonAnnotation
from src.backend.enums.annotation_type import AnnotationType


def test_polygon_annotation_creation() -> None:
    points = [(0.1, 0.2), (0.3, 0.4), (0.5, 0.6)]
    polygon = PolygonAnnotation(class_index=1, points=points)
    assert polygon.class_index == 1
    assert polygon.points == points


def test_polygon_annotation_type() -> None:
    polygon = PolygonAnnotation(class_index=0, points=[(0.1, 0.2)])
    assert polygon.annotation_type == AnnotationType.POLYGON


def test_polygon_to_yolo_line() -> None:
    points = [(0.1, 0.2), (0.3, 0.4)]
    polygon = PolygonAnnotation(class_index=1, points=points)
    yolo_line = polygon.to_yolo_line()
    assert yolo_line == '1 0.1 0.2 0.3 0.4'


def test_polygon_from_yolo_line() -> None:
    line = '0 0.1 0.2 0.3 0.4 0.5 0.6'
    polygon = PolygonAnnotation.from_yolo_line(line)
    assert polygon.class_index == 0
    assert polygon.points == [(0.1, 0.2), (0.3, 0.4), (0.5, 0.6)]


def test_polygon_roundtrip() -> None:
    original = PolygonAnnotation(class_index=2, points=[(0.1, 0.2), (0.3, 0.4), (0.5, 0.6)])
    line = original.to_yolo_line()
    restored = PolygonAnnotation.from_yolo_line(line)
    assert original.class_index == restored.class_index
    assert original.points == restored.points


def test_polygon_empty_points() -> None:
    polygon = PolygonAnnotation(class_index=0, points=[])
    yolo_line = polygon.to_yolo_line()
    assert yolo_line == '0 '

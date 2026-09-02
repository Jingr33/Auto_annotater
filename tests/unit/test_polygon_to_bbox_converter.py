import pytest

from backend.annotations.bbox_annotation import BBoxAnnotation
from backend.annotations.polygon_annotation import PolygonAnnotation
from backend.annotations.polygon_to_bbox_converter import PolygonToBboxConverter


def test_convert_polygon_to_bbox_basic() -> None:
    points = [(0.1, 0.2), (0.3, 0.4), (0.5, 0.6)]
    polygon = PolygonAnnotation(class_index=0, points=points)
    bbox = PolygonToBboxConverter.convert(polygon)
    assert isinstance(bbox, BBoxAnnotation)
    assert bbox.class_index == 0
    assert bbox.x == pytest.approx(0.1)
    assert bbox.y == pytest.approx(0.2)
    assert bbox.width == pytest.approx(0.4)
    assert bbox.height == pytest.approx(0.4)


def test_convert_polygon_to_bbox_single_point() -> None:
    points = [(0.5, 0.5)]
    polygon = PolygonAnnotation(class_index=1, points=points)
    bbox = PolygonToBboxConverter.convert(polygon)
    assert bbox.class_index == 1
    assert bbox.x == pytest.approx(0.5)
    assert bbox.y == pytest.approx(0.5)
    assert bbox.width == pytest.approx(0.0)
    assert bbox.height == pytest.approx(0.0)


def test_convert_polygon_to_bbox_empty_points() -> None:
    polygon = PolygonAnnotation(class_index=2, points=[])
    bbox = PolygonToBboxConverter.convert(polygon)
    assert bbox.class_index == 2
    assert bbox.x == 0.0
    assert bbox.y == 0.0
    assert bbox.width == 0.0
    assert bbox.height == 0.0


def test_convert_polygon_to_bbox_negative_coords() -> None:
    points = [(-0.5, -0.3), (0.2, 0.4)]
    polygon = PolygonAnnotation(class_index=3, points=points)
    bbox = PolygonToBboxConverter.convert(polygon)
    assert bbox.x == pytest.approx(-0.5)
    assert bbox.y == pytest.approx(-0.3)
    assert bbox.width == pytest.approx(0.7)
    assert bbox.height == pytest.approx(0.7)

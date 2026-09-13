import os
import tempfile

from backend.annotations.annotation_parser import AnnotationParser
from backend.annotations.bbox_annotation import BBoxAnnotation
from backend.annotations.polygon_annotation import PolygonAnnotation


def test_load_nonexistent_file() -> None:
    result = AnnotationParser.load('/nonexistent/path.txt')
    assert result == []


def test_load_bbox_annotations() -> None:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('0 0.5 0.5 0.2 0.3\n')
        f.write('1 0.1 0.2 0.3 0.4\n')
        f_path = f.name

    try:
        annotations = AnnotationParser.load(f_path)
        assert len(annotations) == 2
        assert isinstance(annotations[0], BBoxAnnotation)
        assert isinstance(annotations[1], BBoxAnnotation)
        assert annotations[0].class_index == 0
        assert annotations[1].class_index == 1
    finally:
        os.unlink(f_path)


def test_load_polygon_annotations() -> None:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('0 0.1 0.2 0.3 0.4 0.5 0.6\n')
        f_path = f.name

    try:
        annotations = AnnotationParser.load(f_path)
        assert len(annotations) == 1
        assert isinstance(annotations[0], PolygonAnnotation)
        assert annotations[0].points == [(0.1, 0.2), (0.3, 0.4), (0.5, 0.6)]
    finally:
        os.unlink(f_path)


def test_load_mixed_annotations() -> None:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('0 0.5 0.5 0.2 0.3\n')
        f.write('1 0.1 0.2 0.3 0.4 0.5 0.6\n')
        f_path = f.name

    try:
        annotations = AnnotationParser.load(f_path)
        assert len(annotations) == 2
        assert isinstance(annotations[0], BBoxAnnotation)
        assert isinstance(annotations[1], PolygonAnnotation)
    finally:
        os.unlink(f_path)


def test_save_and_load_annotations() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, 'annotations.txt')
        annotations = [
            BBoxAnnotation(class_index=0, x=0.5, y=0.5, width=0.2, height=0.3),
            PolygonAnnotation(class_index=1, points=[(0.1, 0.2), (0.3, 0.4), (0.5, 0.6)]),
        ]

        AnnotationParser.save(file_path, annotations)
        loaded = AnnotationParser.load(file_path)

        assert len(loaded) == 2
        assert isinstance(loaded[0], BBoxAnnotation)
        assert isinstance(loaded[1], PolygonAnnotation)


def test_format_string() -> None:
    annotations = [
        BBoxAnnotation(class_index=0, x=0.5, y=0.5, width=0.2, height=0.3),
        PolygonAnnotation(class_index=1, points=[(0.1, 0.2), (0.3, 0.4)]),
    ]
    result = AnnotationParser.format_string(annotations)
    expected = '0 0.5000 0.5000 0.2000 0.3000\n1 0.1000 0.2000 0.3000 0.4000\n'
    assert result == expected


def test_format_string_empty() -> None:
    result = AnnotationParser.format_string([])
    assert result == ''


def test_load_empty_file() -> None:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f_path = f.name

    try:
        annotations = AnnotationParser.load(f_path)
        assert annotations == []
    finally:
        os.unlink(f_path)

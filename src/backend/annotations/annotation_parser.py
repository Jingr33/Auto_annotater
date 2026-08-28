import os

from src.backend.annotations import Annotation
from src.backend.annotations.bbox_annotation import BBoxAnnotation
from src.backend.annotations.polygon_annotation import PolygonAnnotation


class AnnotationParser:
    @staticmethod
    def load(file_path: str) -> list[Annotation]:
        if not os.path.exists(file_path):
            return []
        annotations: list[Annotation] = []
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                annotations.append(AnnotationParser._parse_line(line))
        return annotations

    @staticmethod
    def save(file_path: str, annotations: list[Annotation]) -> None:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            for annot in annotations:
                f.write(annot.to_yolo_line() + '\n')

    @staticmethod
    def format_string(annotations: list[Annotation]) -> str:
        if not annotations:
            return ''
        return '\n'.join(a.to_yolo_line() for a in annotations) + '\n'

    @staticmethod
    def _parse_line(line: str) -> Annotation:
        parts = line.strip().split()
        num_coords = len(parts) - 1
        if num_coords == 4:
            return BBoxAnnotation.from_yolo_line(line)
        elif num_coords >= 6 and num_coords % 2 == 0:
            return PolygonAnnotation.from_yolo_line(line)
        else:
            raise ValueError(f'Unknown annotation format: {line}')

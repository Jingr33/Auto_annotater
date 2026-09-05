from dataclasses import dataclass, field

from backend.enums.annotation_type import AnnotationType


@dataclass
class PolygonAnnotation:
    class_index: int
    points: list[tuple[float, float]] = field(default_factory=list)

    @property
    def annotation_type(self) -> AnnotationType:
        return AnnotationType.POLYGON

    def to_yolo_line(self) -> str:
        coords = ' '.join(f'{x:.4f} {y:.4f}' for x, y in self.points)
        return f'{self.class_index} {coords}'

    @classmethod
    def from_yolo_line(cls, line: str) -> 'PolygonAnnotation':
        parts = line.strip().split()
        class_index = int(parts[0])
        coords = [float(p) for p in parts[1:]]
        points = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
        return cls(class_index=class_index, points=points)

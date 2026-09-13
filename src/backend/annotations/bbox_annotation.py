from dataclasses import dataclass

from backend.enums.annotation_type import AnnotationType


@dataclass
class BBoxAnnotation:
    class_index: int
    x: float
    y: float
    width: float
    height: float

    @property
    def annotation_type(self) -> AnnotationType:
        return AnnotationType.BBOX

    def to_yolo_line(self) -> str:
        return f'{self.class_index} {self.x:.4f} {self.y:.4f} {self.width:.4f} {self.height:.4f}'

    @classmethod
    def from_yolo_line(cls, line: str) -> 'BBoxAnnotation':
        parts = line.strip().split()
        return cls(
            class_index=int(parts[0]),
            x=float(parts[1]),
            y=float(parts[2]),
            width=float(parts[3]),
            height=float(parts[4]),
        )

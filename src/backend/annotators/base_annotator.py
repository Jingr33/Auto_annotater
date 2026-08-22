from abc import ABC, abstractmethod

from backend.annotations import Annotation


class BaseAnnotator(ABC):
    @abstractmethod
    def annotate(self, image_path: str) -> list[Annotation]: ...

    @abstractmethod
    def annotate_with_bbox(self, image_path: str, bbox: tuple[float, float, float, float]) -> list[Annotation]: ...

    @abstractmethod
    def cleanup(self) -> None:
        pass

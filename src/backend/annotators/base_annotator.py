from abc import ABC, abstractmethod

from backend.annotations import Annotation


class BaseAnnotator(ABC):
    @abstractmethod
    def annotate(self, image_path: str) -> list[Annotation]: ...

    @abstractmethod
    def annotate_with_bbox(self, image_path: str, bbox: tuple[float, float, float, float]) -> list[Annotation]: ...

    def annotate_with_point(self, image_path: str, point: tuple[float, float]) -> list[Annotation]:
        raise NotImplementedError(f'{type(self).__name__} does not support point prompts')

    @abstractmethod
    def cleanup(self) -> None:
        pass

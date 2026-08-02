from abc import ABC, abstractmethod
from typing import List, Tuple

from backend.annotations import Annotation


class BaseAnnotator(ABC):
    @abstractmethod
    def annotate(self, image_path: str) -> List[Annotation]:
        ...

    @abstractmethod
    def annotate_with_bbox(
        self, image_path: str, bbox: Tuple[float, float, float, float]
    ) -> List[Annotation]:
        ...

    def annotate_with_point(
        self, image_path: str, point: Tuple[float, float]
    ) -> List[Annotation]:
        raise NotImplementedError(f"{type(self).__name__} does not support point prompts")

    def cleanup(self) -> None:
        ...

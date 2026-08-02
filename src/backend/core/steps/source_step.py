from abc import ABC, abstractmethod
from typing import Generator

from backend.core.frame_dto import FrameDTO


class SourceStep(ABC):
    name: str = "source"

    @abstractmethod
    def run(self) -> Generator[FrameDTO, None, None]:
        ...

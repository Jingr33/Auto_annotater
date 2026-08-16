from abc import ABC, abstractmethod
from collections.abc import Generator

from backend.core.frame_dto import FrameDTO


class SourceStep(ABC):
    @abstractmethod
    def run(self) -> Generator[FrameDTO, None, None]:
        pass

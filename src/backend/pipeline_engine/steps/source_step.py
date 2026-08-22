from abc import ABC, abstractmethod
from collections.abc import Generator

from backend.pipeline_engine.frame_dto import FrameDTO


class SourceStep(ABC):
    @abstractmethod
    def run(self) -> Generator[FrameDTO, None, None]:
        pass

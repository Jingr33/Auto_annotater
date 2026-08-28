from abc import ABC, abstractmethod

from backend.pipeline_engine.frame_dto import FrameDTO


class Step(ABC):
    @abstractmethod
    def process(self, dto: FrameDTO) -> FrameDTO | None:
        pass

    @abstractmethod
    def postprocess(self) -> None:
        pass

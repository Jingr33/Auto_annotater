from abc import ABC, abstractmethod

from backend.core.frame_dto import FrameDTO


class Step(ABC):
    @abstractmethod
    def process(self, dto: FrameDTO) -> FrameDTO | None:
        pass

    def postprocess(self) -> None:
        pass

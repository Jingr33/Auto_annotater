from abc import ABC, abstractmethod

from backend.core.frame_dto import FrameDTO


class Step(ABC):
    name: str = "step"

    @abstractmethod
    def process(self, dto: FrameDTO) -> FrameDTO | None:
        ...

    def postprocess(self) -> None:
        ...

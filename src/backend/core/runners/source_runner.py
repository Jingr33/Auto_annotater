import queue
import threading

from backend.core.frame_dto import FrameDTO
from backend.core.steps.source_step import SourceStep


class SourceRunner(threading.Thread):
    def __init__(
        self,
        step: SourceStep,
        queue_out: queue.Queue[FrameDTO | None],
    ):
        super().__init__(daemon=True)
        self.step = step
        self.queue_out = queue_out

    def run(self) -> None:
        for dto in self.step.run():
            self.queue_out.put(dto)
        self.queue_out.put(None)

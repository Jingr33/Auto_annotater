import queue
import threading
from collections.abc import Callable

from backend.core.frame_dto import FrameDTO
from backend.core.steps.source_step import SourceStep


class SourceRunner(threading.Thread):
    def __init__(
        self,
        step: SourceStep,
        queue_out: queue.Queue[FrameDTO | None],
        on_count: Callable[[int], None] | None = None,
    ):
        super().__init__(daemon=True)
        self.step = step
        self.queue_out = queue_out
        self._on_count = on_count

    def run(self) -> None:
        count = 0
        for dto in self.step.run():
            self.queue_out.put(dto)
            count += 1
        if self._on_count is not None:
            self._on_count(count)
        self.queue_out.put(None)

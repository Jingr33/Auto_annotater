import queue
import threading

from backend.core.frame_dto import FrameDTO
from backend.core.steps.step import Step


class StepRunner(threading.Thread):
    def __init__(
        self,
        step: Step,
        queue_in: queue.Queue[FrameDTO | None],
        queue_out: queue.Queue[FrameDTO | None] | None,
    ):
        super().__init__(daemon=True)
        self.step = step
        self.queue_in = queue_in
        self.queue_out = queue_out

    def run(self) -> None:
        while True:
            dto = self.queue_in.get()
            if dto is None:
                self.queue_in.task_done()
                break
            result = self.step.process(dto)
            if result is not None and self.queue_out is not None:
                self.queue_out.put(result)
            self.queue_in.task_done()
        self.step.postprocess()
        if self.queue_out is not None:
            self.queue_out.put(None)

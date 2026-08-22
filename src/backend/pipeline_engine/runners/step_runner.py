import logging
import queue
import threading

from backend.pipeline_engine.frame_dto import FrameDTO
from backend.pipeline_engine.steps.step import Step

logger = logging.getLogger(__name__)


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
        self.exception: Exception | None = None

    def run(self) -> None:
        try:
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
        except Exception as e:
            self.exception = e
            logger.error('Step %s failed: %s', type(self.step).__name__, e)
            if self.queue_out is not None:
                self.queue_out.put(None)

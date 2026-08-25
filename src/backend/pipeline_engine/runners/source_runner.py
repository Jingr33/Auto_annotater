import logging
import queue
import threading

from backend.pipeline_engine.frame_dto import FrameDTO
from backend.pipeline_engine.steps.source_step import SourceStep

logger = logging.getLogger(__name__)


class SourceRunner(threading.Thread):
    def __init__(
        self,
        step: SourceStep,
        queue_out: queue.Queue[FrameDTO | None],
    ):
        super().__init__(daemon=True)
        self.step = step
        self.queue_out = queue_out
        self.exception: Exception | None = None

    def run(self) -> None:
        try:
            for dto in self.step.run():
                self.queue_out.put(dto)
            self.queue_out.put(None)
        except Exception as e:
            self.exception = e
            logger.error('Source step failed: %s', e)
            self.queue_out.put(None)

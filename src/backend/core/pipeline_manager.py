import queue
import threading
from typing import List

from backend.core.frame_dto import FrameDTO
from backend.core.steps.source_step import SourceStep
from backend.core.steps.step import Step
from backend.core.runners.source_runner import SourceRunner
from backend.core.runners.step_runner import StepRunner
from backend.core.data_manager import DataManager
from backend.enums.image_prediction_status import ImagePredictionStatus
from config import QUEUE_MAXSIZE


class PipelineManager:
    def __init__(
        self,
        source_step: SourceStep | None,
        pipeline_steps: List[Step],
        workspace: str,
        with_frontend: bool = False,
        only_pending: bool = True,
    ):
        self.data_manager = DataManager(workspace)
        self.only_pending = only_pending

        n_queues = len(pipeline_steps) + (1 if with_frontend else 0)
        queues = [queue.Queue(maxsize=QUEUE_MAXSIZE) for _ in range(n_queues)]

        if source_step is None:
            self._source_runner = threading.Thread(
                target=self._enqueue_pending_items,
                args=(queues[0],),
                daemon=True,
            )
        else:
            self._source_runner = SourceRunner(source_step, queues[0])

        self._step_runners: List[StepRunner] = []
        for i, step in enumerate(pipeline_steps):
            runner = StepRunner(
                step=step,
                queue_in=queues[i],
                queue_out=queues[i + 1] if i + 1 < len(queues) else None,
            )
            self._step_runners.append(runner)

        self._frontend_queue = queues[-1] if with_frontend else None
        self._current_dto: FrameDTO | None = None
        self._history: list[str] = []
        self._total = 0
        self._started = False

    def start(self) -> None:
        self._source_runner.start()
        for r in self._step_runners:
            r.start()
        self._started = True

    def wait(self) -> None:
        self._source_runner.join()
        for runner in self._step_runners:
            runner.join()

    def finalize(self) -> None:
        self.data_manager.close()

    def get_current(self) -> FrameDTO | None:
        if self._current_dto is not None:
            return self._current_dto
        if self._frontend_queue is None:
            return None
        try:
            self._current_dto = self._frontend_queue.get(timeout=0.3)
        except queue.Empty:
            return None
        return self._current_dto if self._current_dto is not None else None

    def is_waiting(self) -> bool:
        alive = self._source_runner.is_alive() or any(r.is_alive() for r in self._step_runners)
        return alive and self._current_dto is None

    def is_finished(self) -> bool:
        queue_done = self._frontend_queue is None or self._frontend_queue.empty()
        return (
            not self._source_runner.is_alive()
            and all(not r.is_alive() for r in self._step_runners)
            and queue_done
            and self._current_dto is None
        )

    def get_total(self) -> int:
        return self._total

    def accept(self) -> None:
        dto = self._current_dto
        if dto is None:
            return
        self._history.append(dto.item_id)
        self.data_manager.set_status(dto.item_id, ImagePredictionStatus.ACCEPTED)
        self._current_dto = None

    def reject(self) -> None:
        dto = self._current_dto
        if dto is None:
            return
        self._history.append(dto.item_id)
        self.data_manager.set_status(dto.item_id, ImagePredictionStatus.REJECTED)
        self._current_dto = None

    def skip(self) -> None:
        if self._current_dto is None:
            return
        self._history.append(self._current_dto.item_id)
        self._current_dto = None

    def back(self) -> bool:
        if not self._history:
            return False
        item_id = self._history.pop()
        self.data_manager.set_status(item_id, ImagePredictionStatus.PENDING)
        self._current_dto = FrameDTO(item_id=item_id, workspace=self.data_manager.workspace)
        return True

    def _enqueue_pending_items(self, output_queue: queue.Queue) -> None:
        if self.only_pending:
            items = self.data_manager.get_items(ImagePredictionStatus.PENDING)
        else:
            items = self.data_manager.get_items()
        self._total = len(items)
        for item in items:
            output_queue.put(
                FrameDTO(item_id=item["id"], workspace=self.data_manager.workspace)
            )
        output_queue.put(None)

import os
import queue
from typing import List

from backend.core.frame_dto import FrameDTO
from backend.core.steps.source_step import SourceStep
from backend.core.steps.step import Step
from backend.core.runners.source_runner import SourceRunner
from backend.core.runners.step_runner import StepRunner
from backend.data_manager import DataManager

QUEUE_MAXSIZE = 200


class PipelineManager:
    def __init__(
        self,
        source_step: SourceStep,
        pipeline_steps: List[Step],
        workspace: str,
        with_frontend: bool = False,
    ):
        self.data_manager = DataManager(workspace)

        n_queues = len(pipeline_steps) + (1 if with_frontend else 0)
        queues = [queue.Queue(maxsize=QUEUE_MAXSIZE) for _ in range(n_queues)]

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

    def finalize(self) -> None:
        rejected = self.data_manager.get_items("rejected")
        for item in rejected:
            self.data_manager.remove_item(item["id"])

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
        self.data_manager.set_status(dto.item_id, "accepted")
        self._current_dto = None

    def reject(self) -> None:
        dto = self._current_dto
        if dto is None:
            return
        self._history.append(dto.item_id)
        self.data_manager.set_status(dto.item_id, "rejected")
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
        self.data_manager.set_status(item_id, "pending")
        self._current_dto = FrameDTO(item_id=item_id, workspace=self.data_manager.workspace)
        return True

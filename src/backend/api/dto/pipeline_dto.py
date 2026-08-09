from dataclasses import dataclass


@dataclass
class PipelineStatusResponseDTO:
    is_waiting: bool
    is_finished: bool
    total: int
    current_item_id: str | None

from typing import Optional

from backend.data_manager import DataManager
from backend.prediction import Prediction


class PredictionManager:
    def __init__(self, workspace: str):
        self.dm = DataManager(workspace)
        self.predictions: list[Prediction] = []
        self.current_id: int = 0
        self._load()

    def get_current(self) -> Optional[Prediction]:
        if not self.predictions:
            return None
        if self.current_id >= len(self.predictions):
            return None
        return self.predictions[self.current_id]

    def get_total(self) -> int:
        return len(self.predictions)

    def is_finished(self) -> bool:
        return self.current_id >= len(self.predictions)

    def accept(self) -> None:
        pred = self.get_current()
        if pred is None:
            return
        self.dm.set_status(pred.item_id, "accepted")
        self.current_id += 1

    def reject(self) -> None:
        pred = self.get_current()
        if pred is None:
            return
        self.dm.set_status(pred.item_id, "rejected")
        self.current_id += 1

    def skip(self) -> None:
        self.current_id += 1

    def back(self) -> bool:
        if self.current_id <= 0:
            return False
        self.current_id -= 1
        pred = self.get_current()
        if pred is None:
            return False
        self.dm.set_status(pred.item_id, "pending")
        return True

    def finalize(self) -> None:
        rejected = self.dm.get_items("rejected")
        for item in rejected:
            self.dm.remove_item(item["id"])

    def _load(self) -> None:
        items = self.dm.get_items("pending")
        for item in items:
            self.predictions.append(Prediction(item["id"], self.dm.workspace))

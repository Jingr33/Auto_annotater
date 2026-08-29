from abc import ABC, abstractmethod


class DatasetPattern(ABC):
    @abstractmethod
    def export_accepted(self, src_item_dir: str, dst_dir: str, item_id: str) -> None:
        pass

    @abstractmethod
    def export_rejected(self, src_item_dir: str, dst_dir: str, item_id: str) -> None:
        pass

import os

from backend.enums.image_prediction_status import ImagePredictionStatus
from backend.enums.model_type import ModelType
from backend.registries import PATTERN_REGISTRY
from config import WORKSPACE_DIR


class DatasetExporter:
    def __init__(self, output_folder: str, model_type: ModelType):
        self.output_folder = os.path.abspath(output_folder)
        self.workspace = os.path.abspath(WORKSPACE_DIR)
        self.pattern = PATTERN_REGISTRY[model_type]

    def export_item(self, item_id: str, status: ImagePredictionStatus) -> None:
        src_item_dir = os.path.join(self.workspace, 'items', item_id)
        if not os.path.exists(src_item_dir):
            return

        if status == ImagePredictionStatus.ACCEPTED:
            self.pattern.export_accepted(src_item_dir, self.output_folder, item_id)
        elif status == ImagePredictionStatus.REJECTED:
            self.pattern.export_rejected(src_item_dir, self.output_folder, item_id)

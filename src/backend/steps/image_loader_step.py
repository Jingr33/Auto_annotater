import os
import shutil
from typing import Generator

from backend.config.image_loader_config import ImageLoaderConfig
from backend.core.frame_dto import FrameDTO
from backend.core.steps.source_step import SourceStep
from backend.core.data_manager import DataManager
from backend.enums.model_type import ModelType


class ImageLoaderStep(SourceStep):
    def __init__(self, config: ImageLoaderConfig):
        self.config = config

    def run(self) -> Generator[FrameDTO, None, None]:
        dm = DataManager(self.config.output_path)
        root = self.config.source_path

        images_dir = os.path.join(root, "images")
        if not os.path.isdir(images_dir):
            images_dir = root

        labels_dir = os.path.join(root, "labels") if os.path.isdir(os.path.join(root, "labels")) else None
        need_bbox = self.config.model_type is ModelType.MEDSAM2 and labels_dir is not None

        for img_file in sorted(os.listdir(images_dir)):
            img_path = os.path.join(images_dir, img_file)
            if not os.path.isfile(img_path):
                continue

            item_id = dm.import_image(img_path)

            if need_bbox:
                name_no_ext = os.path.splitext(img_file)[0]
                txt_path = os.path.join(labels_dir, name_no_ext + ".txt")
                if os.path.exists(txt_path):
                    dst = os.path.join(dm.workspace, "items", item_id, "yolo.txt")
                    shutil.copy2(txt_path, dst)

            yield FrameDTO(item_id=item_id, workspace=self.config.output_path)

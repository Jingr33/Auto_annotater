import os
import shutil
from collections.abc import Generator

from src.backend.config.image_loader_config import ImageLoaderConfig
from src.backend.enums.model_type import ModelType
from src.backend.pipeline_engine.data_manager import DataManager
from src.backend.pipeline_engine.frame_dto import FrameDTO
from src.backend.pipeline_engine.steps.source_step import SourceStep
from src.backend.validators.dataset_validator import DatasetValidator


class ImageLoaderStep(SourceStep):
    def __init__(self, config: ImageLoaderConfig):
        self.config = config
        self._dm: DataManager | None = None

    def run(self) -> Generator[FrameDTO, None, None]:
        dm = DataManager(self.config.output_path)
        self._dm = dm
        root = self.config.source_path

        image_files = DatasetValidator().validate(root, self.config.model_type)
        source_dir = os.path.join(root, 'images')

        labels_dir = os.path.join(root, 'labels') if os.path.isdir(os.path.join(root, 'labels')) else None
        need_bbox = self.config.model_type == ModelType.MEDSAM2 and labels_dir is not None

        for img_file in sorted(image_files):
            img_path = os.path.join(source_dir, img_file)
            item_id = dm.import_image(img_path)

            if need_bbox:
                name_no_ext = os.path.splitext(img_file)[0]
                txt_path = os.path.join(labels_dir, name_no_ext + '.txt')
                if os.path.exists(txt_path):
                    dst = os.path.join(dm.workspace, 'items', item_id, 'yolo.txt')
                    shutil.copy2(txt_path, dst)

            yield FrameDTO(item_id=item_id, workspace=self.config.output_path)

    def close(self) -> None:
        if self._dm is not None:
            self._dm.close()
            self._dm = None

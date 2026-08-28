import gc
import os
import tempfile

from src.backend.config.image_loader_config import ImageLoaderConfig
from src.backend.enums.model_type import ModelType
from src.backend.pipeline_engine.data_manager import DataManager
from src.backend.steps.image_loader_step import ImageLoaderStep


def test_yolo_annotation_workflow() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        source_dir = os.path.join(tmpdir, 'source')
        images_dir = os.path.join(source_dir, 'images')
        os.makedirs(images_dir)

        for i in range(2):
            with open(os.path.join(images_dir, f'img{i}.jpg'), 'w') as f:
                f.write(f'fake image {i}')

        output_dir = os.path.join(tmpdir, 'output')
        config = ImageLoaderConfig(
            source_path=source_dir,
            output_path=output_dir,
            model_type=ModelType.YOLO,
        )

        step = ImageLoaderStep(config)
        frames = list(step.run())
        assert len(frames) == 2
        step.close()

        dm = DataManager(output_dir)
        items = dm.get_items()
        assert len(items) == 2
        dm.close()


def test_image_loader_with_valid_dataset() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        source_dir = os.path.join(tmpdir, 'source')
        images_dir = os.path.join(source_dir, 'images')
        os.makedirs(images_dir)

        for i in range(3):
            with open(os.path.join(images_dir, f'img{i}.jpg'), 'w') as f:
                f.write(f'fake image {i}')

        output_dir = os.path.join(tmpdir, 'output')
        config = ImageLoaderConfig(
            source_path=source_dir,
            output_path=output_dir,
            model_type=ModelType.YOLO,
        )

        step = ImageLoaderStep(config)
        frames = list(step.run())
        assert len(frames) == 3
        step.close()

        dm = DataManager(output_dir)
        items = dm.get_items()
        assert len(items) == 3
        dm.close()


def test_image_loader_with_medsam2_and_labels() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        source_dir = os.path.join(tmpdir, 'source')
        images_dir = os.path.join(source_dir, 'images')
        labels_dir = os.path.join(source_dir, 'labels')
        os.makedirs(images_dir)
        os.makedirs(labels_dir)

        for i in range(2):
            with open(os.path.join(images_dir, f'img{i}.jpg'), 'w') as f:
                f.write(f'fake image {i}')
            with open(os.path.join(labels_dir, f'img{i}.txt'), 'w') as f:
                f.write('0 0.5 0.5 0.2 0.3')

        output_dir = os.path.join(tmpdir, 'output')
        config = ImageLoaderConfig(
            source_path=source_dir,
            output_path=output_dir,
            model_type=ModelType.MEDSAM2,
        )

        step = ImageLoaderStep(config)
        frames = list(step.run())
        assert len(frames) == 2
        step.close()

        dm = DataManager(output_dir)
        items = dm.get_items()
        assert len(items) == 2
        dm.close()

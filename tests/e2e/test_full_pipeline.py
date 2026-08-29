import os
import tempfile

from backend.config.image_loader_config import ImageLoaderConfig
from backend.enums.image_prediction_status import ImagePredictionStatus
from backend.enums.model_type import ModelType
from backend.pipeline_engine.data_manager import DataManager
from backend.pipeline_engine.pipeline_manager import PipelineManager
from backend.steps.image_loader_step import ImageLoaderStep


def test_pipeline_with_source_step() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        source_dir = os.path.join(tmpdir, 'source')
        images_dir = os.path.join(source_dir, 'images')
        os.makedirs(images_dir)

        for i in range(2):
            with open(os.path.join(images_dir, f'img{i}.jpg'), 'w') as f:
                f.write(f'fake image {i}')

        output_dir = os.path.join(tmpdir, 'output')
        loader_config = ImageLoaderConfig(
            source_path=source_dir,
            output_path=output_dir,
            model_type=ModelType.YOLO,
        )
        source_step = ImageLoaderStep(loader_config)

        manager = PipelineManager(
            source_step=source_step,
            pipeline_steps=[],
            workspace=output_dir,
            with_frontend=True,
        )
        manager.start()
        manager.wait()
        manager.accept()
        manager.finalize()
        source_step.close()

        dm = DataManager(output_dir)
        items = dm.get_items()
        assert len(items) == 2
        dm.close()


def test_pipeline_accept_reject_workflow() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        source_dir = os.path.join(tmpdir, 'source')
        images_dir = os.path.join(source_dir, 'images')
        os.makedirs(images_dir)

        for i in range(3):
            with open(os.path.join(images_dir, f'img{i}.jpg'), 'w') as f:
                f.write(f'fake image {i}')

        output_dir = os.path.join(tmpdir, 'output')
        loader_config = ImageLoaderConfig(
            source_path=source_dir,
            output_path=output_dir,
            model_type=ModelType.YOLO,
        )
        source_step = ImageLoaderStep(loader_config)

        manager = PipelineManager(
            source_step=source_step,
            pipeline_steps=[],
            workspace=output_dir,
            with_frontend=True,
        )
        manager.start()
        manager.wait()

        dm = DataManager(output_dir)

        first = manager.get_current()
        assert first is not None
        manager.accept()

        second = manager.get_current()
        assert second is not None
        manager.reject()

        third = manager.get_current()
        assert third is not None
        manager.accept()

        manager.finalize()
        source_step.close()

        accepted = dm.get_items(ImagePredictionStatus.ACCEPTED)
        rejected = dm.get_items(ImagePredictionStatus.REJECTED)
        assert len(accepted) == 2
        assert len(rejected) == 1
        dm.close()

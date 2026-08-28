import os
import tempfile

import pytest

from src.backend.enums.image_prediction_status import ImagePredictionStatus
from src.backend.pipeline_engine.data_manager import DataManager
from src.backend.pipeline_engine.frame_dto import FrameDTO
from src.backend.pipeline_engine.pipeline_manager import PipelineManager


def test_pipeline_manager_accept() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        dm = DataManager(workspace)

        img_path = os.path.join(tmpdir, 'test.jpg')
        with open(img_path, 'w') as f:
            f.write('fake image')
        dm.import_image(img_path)
        dm.close()

        manager = PipelineManager(
            source_step=None,
            pipeline_steps=[],
            workspace=workspace,
            with_frontend=True,
        )

        manager.start()
        manager.wait()

        dto = manager.get_current()
        if dto is not None:
            manager.accept()
            dm2 = DataManager(workspace)
            items = dm2.get_items(ImagePredictionStatus.ACCEPTED)
            assert len(items) == 1
            dm2.close()

        manager.finalize()


def test_pipeline_manager_reject() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        dm = DataManager(workspace)

        img_path = os.path.join(tmpdir, 'test.jpg')
        with open(img_path, 'w') as f:
            f.write('fake image')
        dm.import_image(img_path)
        dm.close()

        manager = PipelineManager(
            source_step=None,
            pipeline_steps=[],
            workspace=workspace,
            with_frontend=True,
        )

        manager.start()
        manager.wait()

        dto = manager.get_current()
        if dto is not None:
            manager.reject()
            dm2 = DataManager(workspace)
            items = dm2.get_items(ImagePredictionStatus.REJECTED)
            assert len(items) == 1
            dm2.close()

        manager.finalize()


def test_pipeline_manager_skip() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        dm = DataManager(workspace)

        img_path = os.path.join(tmpdir, 'test.jpg')
        with open(img_path, 'w') as f:
            f.write('fake image')
        dm.import_image(img_path)
        dm.close()

        manager = PipelineManager(
            source_step=None,
            pipeline_steps=[],
            workspace=workspace,
            with_frontend=True,
        )

        manager.start()
        manager.wait()

        dto = manager.get_current()
        if dto is not None:
            manager.skip()

        dm2 = DataManager(workspace)
        items = dm2.get_items(ImagePredictionStatus.PENDING)
        assert len(items) == 1
        dm2.close()

        manager.finalize()


def test_pipeline_manager_back() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        dm = DataManager(workspace)

        img_path = os.path.join(tmpdir, 'test.jpg')
        with open(img_path, 'w') as f:
            f.write('fake image')
        dm.import_image(img_path)
        dm.close()

        manager = PipelineManager(
            source_step=None,
            pipeline_steps=[],
            workspace=workspace,
            with_frontend=True,
        )

        manager.start()
        manager.wait()

        dto = manager.get_current()
        if dto is not None:
            manager.accept()
            success = manager.back()
            assert success

        manager.finalize()

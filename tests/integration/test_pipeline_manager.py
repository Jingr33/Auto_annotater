import os
import tempfile
from unittest.mock import patch

from backend.enums.image_prediction_status import ImagePredictionStatus
from backend.pipeline_engine.data_manager import DataManager
from backend.pipeline_engine.pipeline_manager import PipelineManager


def test_pipeline_manager_accept() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
            dm = DataManager()

            img_path = os.path.join(tmpdir, 'test.jpg')
            with open(img_path, 'w') as f:
                f.write('fake image')
            dm.import_image(img_path)
            dm.close()

        args = type('Args', (), {'model': None, 'dataset_output': None, 'only_pending': True})()
        manager = PipelineManager(args, with_frontend=True)

        manager.start()
        manager.wait()

        dto = manager.get_current()
        if dto is not None:
            manager.accept()
            with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
                dm2 = DataManager()
                items = dm2.get_items(ImagePredictionStatus.ACCEPTED)
                assert len(items) == 1
                dm2.close()

        manager.finalize()


def test_pipeline_manager_reject() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
            dm = DataManager()

            img_path = os.path.join(tmpdir, 'test.jpg')
            with open(img_path, 'w') as f:
                f.write('fake image')
            dm.import_image(img_path)
            dm.close()

        args = type('Args', (), {'model': None, 'dataset_output': None, 'only_pending': True})()
        manager = PipelineManager(args, with_frontend=True)

        manager.start()
        manager.wait()

        dto = manager.get_current()
        if dto is not None:
            manager.reject()
            with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
                dm2 = DataManager()
                items = dm2.get_items(ImagePredictionStatus.REJECTED)
                assert len(items) == 1
                dm2.close()

        manager.finalize()


def test_pipeline_manager_skip() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
            dm = DataManager()

            img_path = os.path.join(tmpdir, 'test.jpg')
            with open(img_path, 'w') as f:
                f.write('fake image')
            dm.import_image(img_path)
            dm.close()

        args = type('Args', (), {'model': None, 'dataset_output': None, 'only_pending': True})()
        manager = PipelineManager(args, with_frontend=True)

        manager.start()
        manager.wait()

        dto = manager.get_current()
        if dto is not None:
            manager.skip()

        with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
            dm2 = DataManager()
            items = dm2.get_items(ImagePredictionStatus.PENDING)
            assert len(items) == 1
            dm2.close()

        manager.finalize()


def test_pipeline_manager_back() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
            dm = DataManager()

            img_path = os.path.join(tmpdir, 'test.jpg')
            with open(img_path, 'w') as f:
                f.write('fake image')
            dm.import_image(img_path)
            dm.close()

        args = type('Args', (), {'model': None, 'dataset_output': None, 'only_pending': True})()
        manager = PipelineManager(args, with_frontend=True)

        manager.start()
        manager.wait()

        dto = manager.get_current()
        if dto is not None:
            manager.accept()
            success = manager.back()
            assert success

        manager.finalize()

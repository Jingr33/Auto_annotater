import os
import tempfile
from unittest.mock import patch

from backend.annotations.bbox_annotation import BBoxAnnotation
from backend.enums.annotation_label import AnnotationLabel
from backend.enums.image_prediction_status import ImagePredictionStatus
from backend.pipeline_engine.data_manager import DataManager


def test_data_manager_creates_workspace() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
            dm = DataManager()
            assert os.path.isdir(workspace)
            assert os.path.isdir(os.path.join(workspace, 'items'))
            dm.close()


def test_data_manager_import_image() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
            dm = DataManager()

            img_path = os.path.join(tmpdir, 'test.jpg')
            with open(img_path, 'w') as f:
                f.write('fake image')

            item_id = dm.import_image(img_path)
            assert item_id == 'test'
            assert os.path.exists(dm.image_path(item_id))

            items = dm.get_items()
            assert len(items) == 1
            dm.close()


def test_data_manager_import_image_custom_id() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
            dm = DataManager()

            img_path = os.path.join(tmpdir, 'test.jpg')
            with open(img_path, 'w') as f:
                f.write('fake image')

            item_id = dm.import_image(img_path, item_id='custom_id')
            assert item_id == 'custom_id'
            dm.close()


def test_data_manager_save_and_load_annotation() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
            dm = DataManager()

            img_path = os.path.join(tmpdir, 'test.jpg')
            with open(img_path, 'w') as f:
                f.write('fake image')
            dm.import_image(img_path)

            annotations = [
                BBoxAnnotation(class_index=0, x=0.5, y=0.5, width=0.2, height=0.3),
                BBoxAnnotation(class_index=1, x=0.1, y=0.2, width=0.3, height=0.4),
            ]

            path = dm.save_annotation('test', annotations, AnnotationLabel.YOLO)
            assert os.path.exists(path)

            loaded = dm.load_annotation('test', AnnotationLabel.YOLO)
            assert len(loaded) == 2
            assert loaded[0].class_index == 0
            assert loaded[1].class_index == 1
            dm.close()


def test_data_manager_set_status() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
            dm = DataManager()

            img_path = os.path.join(tmpdir, 'test.jpg')
            with open(img_path, 'w') as f:
                f.write('fake image')
            dm.import_image(img_path)

            dm.set_status('test', ImagePredictionStatus.ACCEPTED)
            items = dm.get_items(ImagePredictionStatus.ACCEPTED)
            assert len(items) == 1

            dm.set_status('test', ImagePredictionStatus.REJECTED)
            items = dm.get_items(ImagePredictionStatus.REJECTED)
            assert len(items) == 1
            dm.close()


def test_data_manager_get_items_with_status_filter() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        with patch('backend.pipeline_engine.data_manager.WORKSPACE_DIR', workspace):
            dm = DataManager()

            for i in range(3):
                img_path = os.path.join(tmpdir, f'img{i}.jpg')
                with open(img_path, 'w') as f:
                    f.write('fake image')
                dm.import_image(img_path)

            dm.set_status('img0', ImagePredictionStatus.ACCEPTED)
            dm.set_status('img1', ImagePredictionStatus.REJECTED)

            pending = dm.get_items(ImagePredictionStatus.PENDING)
            assert len(pending) == 1

            accepted = dm.get_items(ImagePredictionStatus.ACCEPTED)
            assert len(accepted) == 1

            all_items = dm.get_items()
            assert len(all_items) == 3
            dm.close()

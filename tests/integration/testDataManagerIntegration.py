import os
import tempfile

from src.backend.annotations.bbox_annotation import BBoxAnnotation
from src.backend.annotations.polygon_annotation import PolygonAnnotation
from src.backend.enums.annotation_label import AnnotationLabel
from src.backend.enums.image_prediction_status import ImagePredictionStatus
from src.backend.pipeline_engine.data_manager import DataManager


def test_data_manager_full_workflow() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        dm = DataManager(workspace)

        images = []
        for i in range(5):
            img_path = os.path.join(tmpdir, f'img{i}.jpg')
            with open(img_path, 'w') as f:
                f.write(f'fake image {i}')
            item_id = dm.import_image(img_path)
            images.append(item_id)

        assert len(dm.get_items()) == 5
        assert len(dm.get_items(ImagePredictionStatus.PENDING)) == 5

        for i, item_id in enumerate(images[:2]):
            dm.set_status(item_id, ImagePredictionStatus.ACCEPTED)

        dm.set_status(images[2], ImagePredictionStatus.REJECTED)

        assert len(dm.get_items(ImagePredictionStatus.PENDING)) == 2
        assert len(dm.get_items(ImagePredictionStatus.ACCEPTED)) == 2
        assert len(dm.get_items(ImagePredictionStatus.REJECTED)) == 1

        annotations = [
            BBoxAnnotation(class_index=0, x=0.5, y=0.5, width=0.2, height=0.3),
            PolygonAnnotation(class_index=1, points=[(0.1, 0.2), (0.3, 0.4)]),
        ]

        for item_id in images:
            dm.save_annotation(item_id, annotations, AnnotationLabel.YOLO)
            loaded = dm.load_annotation(item_id, AnnotationLabel.YOLO)
            assert len(loaded) == 2

        dm.close()


def test_data_manager_annotation_persistence() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = os.path.join(tmpdir, 'workspace')
        dm = DataManager(workspace)

        img_path = os.path.join(tmpdir, 'test.jpg')
        with open(img_path, 'w') as f:
            f.write('fake image')
        item_id = dm.import_image(img_path)

        bbox = BBoxAnnotation(class_index=0, x=0.5, y=0.5, width=0.2, height=0.3)
        dm.save_annotation(item_id, [bbox], AnnotationLabel.YOLO)
        dm.close()

        dm2 = DataManager(workspace)
        loaded = dm2.load_annotation(item_id, AnnotationLabel.YOLO)
        assert len(loaded) == 1
        assert loaded[0].class_index == 0
        dm2.close()

import os
import tempfile

import pytest

from backend.enums.model_type import ModelType
from backend.validators.dataset_validator import DatasetValidator


def test_validate_nonexistent_path() -> None:
    validator = DatasetValidator()
    with pytest.raises(FileNotFoundError, match='Source path does not exist'):
        validator.validate('/nonexistent/path', ModelType.YOLO)


def test_validate_missing_images_dir() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        validator = DatasetValidator()
        with pytest.raises(FileNotFoundError, match='Required images/ folder not found'):
            validator.validate(tmpdir, ModelType.YOLO)


def test_validate_empty_images_dir() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, 'images'))
        validator = DatasetValidator()
        with pytest.raises(FileNotFoundError, match='No image files found'):
            validator.validate(tmpdir, ModelType.YOLO)


def test_validate_valid_yolo_dataset() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        images_dir = os.path.join(tmpdir, 'images')
        os.makedirs(images_dir)
        for i in range(3):
            with open(os.path.join(images_dir, f'img{i}.jpg'), 'w') as f:
                f.write('fake image')

        validator = DatasetValidator()
        result = validator.validate(tmpdir, ModelType.YOLO)
        assert len(result) == 3
        assert 'img0.jpg' in result


def test_validate_medsam2_requires_labels_dir() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        images_dir = os.path.join(tmpdir, 'images')
        os.makedirs(images_dir)
        with open(os.path.join(images_dir, 'img.jpg'), 'w') as f:
            f.write('fake image')

        validator = DatasetValidator()
        with pytest.raises(FileNotFoundError, match='MEDSAM2 dataset requires a labels/ folder'):
            validator.validate(tmpdir, ModelType.MEDSAM2)


def test_validate_medsam2_valid_dataset() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        images_dir = os.path.join(tmpdir, 'images')
        labels_dir = os.path.join(tmpdir, 'labels')
        os.makedirs(images_dir)
        os.makedirs(labels_dir)

        with open(os.path.join(images_dir, 'img.jpg'), 'w') as f:
            f.write('fake image')
        with open(os.path.join(labels_dir, 'img.txt'), 'w') as f:
            f.write('0 0.5 0.5 0.2 0.3')

        validator = DatasetValidator()
        result = validator.validate(tmpdir, ModelType.MEDSAM2)
        assert len(result) == 1
        assert 'img.jpg' in result


def test_validate_medsam2_empty_label_file() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        images_dir = os.path.join(tmpdir, 'images')
        labels_dir = os.path.join(tmpdir, 'labels')
        os.makedirs(images_dir)
        os.makedirs(labels_dir)

        with open(os.path.join(images_dir, 'img.jpg'), 'w') as f:
            f.write('fake image')
        with open(os.path.join(labels_dir, 'img.txt'), 'w') as f:
            f.write('')

        validator = DatasetValidator()
        with pytest.raises(ValueError, match='MEDSAM2 label is empty'):
            validator.validate(tmpdir, ModelType.MEDSAM2)


def test_validate_medsam2_invalid_bbox_values() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        images_dir = os.path.join(tmpdir, 'images')
        labels_dir = os.path.join(tmpdir, 'labels')
        os.makedirs(images_dir)
        os.makedirs(labels_dir)

        with open(os.path.join(images_dir, 'img.jpg'), 'w') as f:
            f.write('fake image')
        with open(os.path.join(labels_dir, 'img.txt'), 'w') as f:
            f.write('0 1.5 0.5 0.2 0.3')

        validator = DatasetValidator()
        with pytest.raises(ValueError, match='between 0 and 1'):
            validator.validate(tmpdir, ModelType.MEDSAM2)


def test_validate_medsam2_zero_width_bbox() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        images_dir = os.path.join(tmpdir, 'images')
        labels_dir = os.path.join(tmpdir, 'labels')
        os.makedirs(images_dir)
        os.makedirs(labels_dir)

        with open(os.path.join(images_dir, 'img.jpg'), 'w') as f:
            f.write('fake image')
        with open(os.path.join(labels_dir, 'img.txt'), 'w') as f:
            f.write('0 0.5 0.5 0.0 0.3')

        validator = DatasetValidator()
        with pytest.raises(ValueError, match='width and height must be greater than zero'):
            validator.validate(tmpdir, ModelType.MEDSAM2)


def test_validate_medsam2_bbox_out_of_bounds() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        images_dir = os.path.join(tmpdir, 'images')
        labels_dir = os.path.join(tmpdir, 'labels')
        os.makedirs(images_dir)
        os.makedirs(labels_dir)

        with open(os.path.join(images_dir, 'img.jpg'), 'w') as f:
            f.write('fake image')
        with open(os.path.join(labels_dir, 'img.txt'), 'w') as f:
            f.write('0 0.9 0.9 0.3 0.3')

        validator = DatasetValidator()
        with pytest.raises(ValueError, match='within image bounds'):
            validator.validate(tmpdir, ModelType.MEDSAM2)


def test_validate_dataset_with_mixed_extensions() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        images_dir = os.path.join(tmpdir, 'images')
        os.makedirs(images_dir)

        with open(os.path.join(images_dir, 'img.jpg'), 'w') as f:
            f.write('fake image')
        with open(os.path.join(images_dir, 'img.png'), 'w') as f:
            f.write('fake image')
        with open(os.path.join(images_dir, 'img.bmp'), 'w') as f:
            f.write('fake image')
        with open(os.path.join(images_dir, 'readme.txt'), 'w') as f:
            f.write('not an image')

        validator = DatasetValidator()
        result = validator.validate(tmpdir, ModelType.YOLO)
        assert len(result) == 3


def test_validate_medsam2_valid_polygon_dataset() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        images_dir = os.path.join(tmpdir, 'images')
        labels_dir = os.path.join(tmpdir, 'labels')
        os.makedirs(images_dir)
        os.makedirs(labels_dir)

        with open(os.path.join(images_dir, 'img.jpg'), 'w') as f:
            f.write('fake image')
        with open(os.path.join(labels_dir, 'img.txt'), 'w') as f:
            f.write('0 0.1 0.2 0.3 0.4 0.5 0.6')

        validator = DatasetValidator()
        result = validator.validate(tmpdir, ModelType.MEDSAM2)
        assert len(result) == 1
        assert 'img.jpg' in result


def test_validate_medsam2_polygon_out_of_bounds() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        images_dir = os.path.join(tmpdir, 'images')
        labels_dir = os.path.join(tmpdir, 'labels')
        os.makedirs(images_dir)
        os.makedirs(labels_dir)

        with open(os.path.join(images_dir, 'img.jpg'), 'w') as f:
            f.write('fake image')
        with open(os.path.join(labels_dir, 'img.txt'), 'w') as f:
            f.write('0 0.1 0.2 1.5 0.4 0.5 0.6')

        validator = DatasetValidator()
        with pytest.raises(ValueError, match='between 0 and 1'):
            validator.validate(tmpdir, ModelType.MEDSAM2)


def test_validate_medsam2_invalid_annotation_format() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        images_dir = os.path.join(tmpdir, 'images')
        labels_dir = os.path.join(tmpdir, 'labels')
        os.makedirs(images_dir)
        os.makedirs(labels_dir)

        with open(os.path.join(images_dir, 'img.jpg'), 'w') as f:
            f.write('fake image')
        with open(os.path.join(labels_dir, 'img.txt'), 'w') as f:
            f.write('0 0.1 0.2 0.3')

        validator = DatasetValidator()
        with pytest.raises(ValueError, match='expected 5 values'):
            validator.validate(tmpdir, ModelType.MEDSAM2)

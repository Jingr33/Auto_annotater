import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_dataset(temp_dir):
    source_dir = os.path.join(temp_dir, 'source')
    images_dir = os.path.join(source_dir, 'images')
    os.makedirs(images_dir)

    for i in range(3):
        with open(os.path.join(images_dir, f'img{i}.jpg'), 'w') as f:
            f.write(f'fake image {i}')

    return source_dir


@pytest.fixture
def sample_dataset_with_labels(temp_dir):
    source_dir = os.path.join(temp_dir, 'source')
    images_dir = os.path.join(source_dir, 'images')
    labels_dir = os.path.join(source_dir, 'labels')
    os.makedirs(images_dir)
    os.makedirs(labels_dir)

    for i in range(3):
        with open(os.path.join(images_dir, f'img{i}.jpg'), 'w') as f:
            f.write(f'fake image {i}')
        with open(os.path.join(labels_dir, f'img{i}.txt'), 'w') as f:
            f.write('0 0.5 0.5 0.2 0.3')

    return source_dir

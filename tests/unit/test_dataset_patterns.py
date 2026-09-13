from pathlib import Path

from backend.pipeline_engine.dataset_patterns.medsam2_pattern import MedSAM2Pattern
from backend.pipeline_engine.dataset_patterns.yolo_pattern import YOLOPattern


def test_medsam2_rejected_export_copies_only_images(tmp_path: Path) -> None:
    source_dir = tmp_path / 'item'
    source_dir.mkdir()
    (source_dir / 'original.jpg').write_bytes(b'image')
    (source_dir / 'sam_polygon.txt').write_text('polygon', encoding='utf-8')
    (source_dir / 'yolo.txt').write_text('bbox', encoding='utf-8')

    MedSAM2Pattern().export_rejected(str(source_dir), str(tmp_path / 'output'), 'item-1')

    rejected_dir = tmp_path / 'output' / 'rejected'
    assert (rejected_dir / 'images' / 'item-1.jpg').exists()
    assert not (rejected_dir / 'labels').exists()
    assert not (rejected_dir / 'bboxes').exists()


def test_yolo_rejected_export_copies_only_images(tmp_path: Path) -> None:
    source_dir = tmp_path / 'item'
    source_dir.mkdir()
    (source_dir / 'original.jpg').write_bytes(b'image')
    (source_dir / 'yolo.txt').write_text('bbox', encoding='utf-8')

    YOLOPattern().export_rejected(str(source_dir), str(tmp_path / 'output'), 'item-1')

    rejected_dir = tmp_path / 'output' / 'rejected'
    assert (rejected_dir / 'images' / 'item-1.jpg').exists()
    assert not (rejected_dir / 'labels').exists()

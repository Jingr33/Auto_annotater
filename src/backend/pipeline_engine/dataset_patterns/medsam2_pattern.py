import os
import shutil

from backend.pipeline_engine.dataset_patterns.base_pattern import DatasetPattern


class MedSAM2Pattern(DatasetPattern):
    def export_accepted(self, src_item_dir: str, dst_dir: str, item_id: str) -> None:
        images_dir = os.path.join(dst_dir, 'images')
        labels_dir = os.path.join(dst_dir, 'labels')
        bboxes_dir = os.path.join(dst_dir, 'bboxes')
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)
        os.makedirs(bboxes_dir, exist_ok=True)

        src_image = os.path.join(src_item_dir, 'original.jpg')
        src_label = os.path.join(src_item_dir, 'sam_polygon.txt')
        src_bbox = os.path.join(src_item_dir, 'yolo.txt')

        if os.path.exists(src_image):
            shutil.copy2(src_image, os.path.join(images_dir, f'{item_id}.jpg'))
        if os.path.exists(src_label):
            shutil.copy2(src_label, os.path.join(labels_dir, f'{item_id}.txt'))
        if os.path.exists(src_bbox):
            shutil.copy2(src_bbox, os.path.join(bboxes_dir, f'{item_id}.txt'))

    def export_rejected(self, src_item_dir: str, dst_dir: str, item_id: str) -> None:
        rejected_dir = os.path.join(dst_dir, 'rejected')
        images_dir = os.path.join(rejected_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)

        src_image = os.path.join(src_item_dir, 'original.jpg')

        if os.path.exists(src_image):
            shutil.copy2(src_image, os.path.join(images_dir, f'{item_id}.jpg'))

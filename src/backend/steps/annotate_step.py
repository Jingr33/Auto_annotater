import os
from typing import List, Tuple

import numpy as np
from PIL import Image, ImageDraw

from backend.annotators.annotator_factory import AnnotatorFactory
from backend.config.annotate_step_config import AnnotateStepConfig
from backend.config.medsam2_config import MedSAM2Config
from backend.core.frame_dto import FrameDTO
from backend.core.steps.step import Step
from backend.core.data_manager import DataManager
from backend.enums.annotation_label import AnnotationLabel
from backend.enums.model_type import ModelType


class AnnotateStep(Step):
    def __init__(self, config: AnnotateStepConfig):
        self.config = config
        self._annotator = None
        self._is_medsam = config.model_type == ModelType.MEDSAM2
        if self._is_medsam:
            self._medsam_root = os.path.join(config.source_workspace, "medsam_dataset")
            self._medsam_image_size = config.medsam_image_size
            self._ensure_medsam_dirs()

    def _ensure_medsam_dirs(self) -> None:
        for sub in [MedSAM2Config.IMGS_FOLDER, MedSAM2Config.GTS_FOLDER, MedSAM2Config.BOXES_FOLDER, MedSAM2Config.LABELS_RECT_FOLDER]:
            os.makedirs(os.path.join(self._medsam_root, sub), exist_ok=True)

    def _lazy_init(self):
        if self._annotator is None:
            self._annotator = AnnotatorFactory.create(self.config)
        return self._annotator

    def process(self, dto: FrameDTO) -> FrameDTO | None:
        dm = DataManager(dto.workspace)
        image_path = dm.image_path(dto.item_id)
        annotator = self._lazy_init()
        annotations = annotator.annotate(image_path)
        label = AnnotationLabel.from_model(self.config.model_type)
        dm.save_annotation(dto.item_id, annotations, label=label)

        if self._is_medsam:
            self._export_medsam_item(dto.item_id, dm)

        return dto

    def postprocess(self) -> None:
        if self._annotator is not None:
            self._annotator.cleanup()
        if self._is_medsam:
            self._generate_labels_rect()

    def _export_medsam_item(self, item_id: str, dm: DataManager) -> None:
        image_path = dm.image_path(item_id)
        if not os.path.isfile(image_path):
            return

        img = Image.open(image_path).convert("RGB")
        img_w, img_h = img.size

        self._save_medsam_image(item_id, img)

        annotations = dm.load_annotation(item_id, label=AnnotationLabel.SAM_POLYGON)
        if not annotations:
            annotations = dm.load_annotation(item_id, label=AnnotationLabel.YOLO)
            mask_arr = self._create_mask(annotations, img_w, img_h, is_yolo_bbox=True)
        else:
            mask_arr = self._create_mask(annotations, img_w, img_h, is_yolo_bbox=False)

        obj_ids = np.unique(mask_arr)
        obj_ids = obj_ids[obj_ids > 0]

        for obj_id in obj_ids:
            mask_bin = (mask_arr == obj_id).astype(np.uint8)

            gts_dir = os.path.join(self._medsam_root, MedSAM2Config.GTS_FOLDER, f"gts_obj{obj_id}")
            os.makedirs(gts_dir, exist_ok=True)
            np.save(os.path.join(gts_dir, item_id + ".npy"), mask_bin)

            boxes_dir = os.path.join(self._medsam_root, MedSAM2Config.BOXES_FOLDER, f"boxes_obj{obj_id}")
            os.makedirs(boxes_dir, exist_ok=True)
            bbox = self._bbox_from_mask(mask_bin)
            if bbox is not None:
                np.save(os.path.join(boxes_dir, item_id + ".npy"), bbox)
            else:
                np.save(os.path.join(boxes_dir, item_id + ".npy"), np.array([], dtype=int))

        self._save_gt_overlay(item_id, img, mask_arr, obj_ids)

    def _generate_labels_rect(self) -> None:
        dm = DataManager(self.config.source_workspace)
        items = dm.get_items()
        for item in items:
            item_id = item["id"]
            annotations = dm.load_annotation(item_id, label=AnnotationLabel.SAM_POLYGON)
            if not annotations:
                continue

            image_path = dm.image_path(item_id)
            if not os.path.isfile(image_path):
                continue

            img = Image.open(image_path)
            img_w, img_h = img.size

            out_path = os.path.join(
                self._medsam_root, MedSAM2Config.LABELS_RECT_FOLDER, item_id + ".txt"
            )
            with open(out_path, "w", encoding="utf-8") as f:
                for annot in annotations:
                    if hasattr(annot, "points") and annot.points:
                        bbox = self._polygon_to_yolo_bbox(annot.points, img_w, img_h)
                        if bbox is not None:
                            f.write(f"{annot.class_index} {bbox}\n")

    def _save_medsam_image(self, base_name: str, img: Image.Image) -> None:
        img_resized = img.resize(
            (self._medsam_image_size, self._medsam_image_size), Image.BICUBIC
        )
        img_arr = np.array(img_resized, dtype=np.float32) / 255.0
        np.save(
            os.path.join(self._medsam_root, MedSAM2Config.IMGS_FOLDER, base_name + ".npy"),
            img_arr,
        )

    def _create_mask(
        self,
        annotations: list,
        img_w: int,
        img_h: int,
        is_yolo_bbox: bool = False,
    ) -> np.ndarray:
        mask_pil = Image.new("L", (img_w, img_h), 0)
        draw = ImageDraw.Draw(mask_pil)

        for annot in annotations:
            cls = annot.class_index + 1
            if is_yolo_bbox and hasattr(annot, "x"):
                cx = annot.x * img_w
                cy = annot.y * img_h
                w = annot.width * img_w
                h = annot.height * img_h
                x1 = int(round(cx - w / 2))
                y1 = int(round(cy - h / 2))
                x2 = int(round(cx + w / 2))
                y2 = int(round(cy + h / 2))
                draw.rectangle([x1, y1, x2, y2], fill=cls if cls < 256 else 255)
            elif hasattr(annot, "points"):
                pts = [
                    (int(round(x * img_w)), int(round(y * img_h)))
                    for x, y in annot.points
                ]
                if len(pts) >= 3:
                    draw.polygon(pts, fill=cls if cls < 256 else 255)

        return np.array(mask_pil, dtype=np.uint8)

    def _save_gt_overlay(
        self,
        base_name: str,
        img_pil: Image.Image,
        mask_arr: np.ndarray,
        obj_ids: np.ndarray,
    ) -> None:
        overlay_dir = os.path.join(self._medsam_root, MedSAM2Config.GTS_FOLDER, "all")
        os.makedirs(overlay_dir, exist_ok=True)

        img_rgba = img_pil.resize(
            (self._medsam_image_size, self._medsam_image_size), Image.BICUBIC
        ).convert("RGBA")
        mask_resized = np.array(
            Image.fromarray(mask_arr).resize(
                (self._medsam_image_size, self._medsam_image_size), Image.NEAREST
            )
        )

        overlay = np.zeros((*img_rgba.size[::-1], 4), dtype=np.uint8)
        for obj_id in obj_ids:
            mask_bin = mask_resized == obj_id
            if not mask_bin.any():
                continue
            color = MedSAM2Config.GT_COLORS[(obj_id - 1) % len(MedSAM2Config.GT_COLORS)]
            overlay[mask_bin] = (*color, 102)

        overlay_pil = Image.fromarray(overlay)
        result = Image.alpha_composite(img_rgba, overlay_pil)
        result.save(os.path.join(overlay_dir, f"{base_name}.png"))

    @staticmethod
    def _bbox_from_mask(mask_bin: np.ndarray) -> np.ndarray | None:
        ys, xs = np.where(mask_bin > 0)
        if xs.size == 0 or ys.size == 0:
            return None
        x1, y1 = int(xs.min()), int(ys.min())
        x2, y2 = int(xs.max()) + 1, int(ys.max()) + 1
        H, W = mask_bin.shape
        x1 = max(0, min(x1, W - 1))
        x2 = max(1, min(x2, W))
        y1 = max(0, min(y1, H - 1))
        y2 = max(1, min(y2, H))
        return np.array([x1, y1, x2, y2], dtype=int)

    @staticmethod
    def _polygon_to_yolo_bbox(
        points: List[Tuple[float, float]], img_w: int, img_h: int
    ) -> str | None:
        if len(points) < 3:
            return None
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x = min(xs) * img_w
        max_x = max(xs) * img_w
        min_y = min(ys) * img_h
        max_y = max(ys) * img_h
        cx = ((min_x + max_x) / 2.0) / img_w
        cy = ((min_y + max_y) / 2.0) / img_h
        w = (max_x - min_x) / img_w
        h = (max_y - min_y) / img_h
        return f"{cx:.10f} {cy:.10f} {w:.10f} {h:.10f}"

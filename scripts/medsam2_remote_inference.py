"""MedSAM2 remote inference script.

This script is uploaded to the remote cluster and executed there.
Custom inference scripts must follow the same interface:

Required arguments:
    --image PATH          Path to the input image
    --result PATH         Path to write the output JSON
    --base-model PATH     Path to base SAM model weights
    --model PATH          Path to fine-tuned model weights
    --bbox X,Y,W,H        Bounding box (normalized coordinates)

Optional arguments:
    --class-index INT     Class index (default: 0)

Output format (written to --result):
    {"polygons": [{"class_index": int, "points": [[x, y], ...]}]}
    Coordinates are normalized to [0, 1] relative to original image size.
"""
import json
import os
from typing import Any

import cv2
import numpy as np
import torch
import torch.nn.functional as F

from src.custom_seg_model import MedSAMCustom, load_sam_checkpoint


IMAGE_SIZE = 1024
DEVICE = "cuda:0"


def parse_bbox(value: str) -> tuple[float, float, float, float]:
    values = [float(part) for part in value.split(",")]
    return values[0], values[1], values[2], values[3]


def load_image(image_path: str) -> tuple[torch.Tensor, tuple[int, int]]:
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image could not be read: {image_path}")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    original_height, original_width = image.shape[:2]
    resized = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
    normalized = resized.astype(np.float32) / 255.0
    tensor = torch.from_numpy(normalized).permute(2, 0, 1).unsqueeze(0)
    return tensor, (original_width, original_height)


def mask_to_polygons(
    mask: np.ndarray,
    width: int,
    height: int,
    class_index: int,
) -> list[dict[str, Any]]:
    contours, _ = cv2.findContours(
        mask.astype(np.uint8),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    polygons = []
    for contour in contours:
        if cv2.contourArea(contour) <= 1:
            continue
        points = [
            [float(point[0][0]) / width, float(point[0][1]) / height]
            for point in contour
        ]
        if len(points) >= 3:
            polygons.append({"class_index": class_index, "points": points})
    return polygons


def infer(args: argparse.Namespace) -> None:
    model = MedSAMCustom.from_config(
        img_size=IMAGE_SIZE,
        freeze_prompt_encoder=True,
    ).to(DEVICE)
    load_sam_checkpoint(model, args.base_model, DEVICE)
    checkpoint = torch.load(args.model, map_location=DEVICE)
    model.load_state_dict(checkpoint["model"])
    model.eval()

    image_tensor, (width, height) = load_image(args.image)
    image_tensor = image_tensor.to(DEVICE)
    x, y, box_width, box_height = parse_bbox(args.bbox)
    box = np.array(
        [[
            (x - box_width / 2) * IMAGE_SIZE,
            (y - box_height / 2) * IMAGE_SIZE,
            (x + box_width / 2) * IMAGE_SIZE,
            (y + box_height / 2) * IMAGE_SIZE,
        ]],
        dtype=np.float32,
    )

    with torch.no_grad():
        mask, _ = model.forward_with_confidence(image_tensor, box)
        mask = torch.sigmoid(mask)
        mask = (mask > 0.8).float()
        mask = F.interpolate(mask, size=(height, width), mode="nearest")

    polygons = mask_to_polygons(
        mask.squeeze().cpu().numpy(),
        width,
        height,
        args.class_index,
    )
    os.makedirs(os.path.dirname(args.result), exist_ok=True)
    with open(args.result, "w", encoding="utf-8") as result_file:
        json.dump({"polygons": polygons}, result_file)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--bbox", required=True)
    parser.add_argument("--class-index", type=int, default=0)
    infer(parser.parse_args())


if __name__ == "__main__":
    main()

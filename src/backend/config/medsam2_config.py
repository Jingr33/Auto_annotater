import os


class MedSAM2Config:
    MODEL_PATH = os.path.join("models", "medsam2.pt")
    IMAGE_SIZE = 1024

    IMGS_FOLDER = "imgs"
    GTS_FOLDER = "gts"
    BOXES_FOLDER = "boxes"
    LABELS_RECT_FOLDER = "labels_rect"

    GT_COLORS = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
        (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
    ]

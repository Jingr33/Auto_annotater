import os


class YOLOConfig:
    MODEL_PATH = os.path.join("models", "dataset4nano.pt")
    CLASSES_OF_INTEREST = [1, 3]

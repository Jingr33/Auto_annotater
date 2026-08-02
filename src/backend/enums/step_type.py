from enum import Enum


class StepType(str, Enum):
    IMAGE_LOADER = "IMAGE_LOADER"
    ANNOTATE = "ANNOTATE"
    SELECT = "SELECT"

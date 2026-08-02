import importlib

from backend.config.annotate_step_config import AnnotateStepConfig
from backend.config.image_loader_config import ImageLoaderConfig
from backend.enums.step_type import StepType


STEP_REGISTRY = {
    StepType.IMAGE_LOADER: ("backend.steps.image_loader_step", "ImageLoaderStep"),
    StepType.ANNOTATE: ("backend.steps.annotate_step", "AnnotateStep"),
}


def create_step(name: StepType, config):
    module_path, class_name = STEP_REGISTRY[name]
    mod = importlib.import_module(module_path)
    return getattr(mod, class_name)(config)

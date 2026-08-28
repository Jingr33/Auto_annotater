import importlib

from src.backend.enums.step_type import StepType


class StepRegistry:
    _registry = {
        StepType.LOAD: ('src.backend.steps.image_loader_step', 'ImageLoaderStep'),
        StepType.ANNOTATE: ('src.backend.steps.annotate_step', 'AnnotateStep'),
    }

    @staticmethod
    def create_step(name: StepType, config):
        module_path, class_name = StepRegistry._registry[name]
        mod = importlib.import_module(module_path)
        return getattr(mod, class_name)(config)

from backend.enums.step_type import StepType
from backend.pipeline_engine.registry import StepRegistry
from backend.steps.annotate_step import AnnotateStep
from backend.steps.image_loader_step import ImageLoaderStep


def test_registry_creates_load_step() -> None:
    from backend.config.image_loader_config import ImageLoaderConfig

    config = ImageLoaderConfig(source_path='/data')
    step = StepRegistry.create_step(StepType.LOAD, config)
    assert isinstance(step, ImageLoaderStep)


def test_registry_creates_annotate_step() -> None:
    from backend.config.annotate_step_config import AnnotateStepConfig
    from backend.enums.model_type import ModelType

    config = AnnotateStepConfig(model_type=ModelType.YOLO)
    step = StepRegistry.create_step(StepType.ANNOTATE, config)
    assert isinstance(step, AnnotateStep)

import sys

from PyQt6.QtWidgets import QApplication

from src.backend.config.annotate_step_config import AnnotateStepConfig
from src.backend.config.image_loader_config import ImageLoaderConfig
from src.backend.config.ssh_config import SSHConfig
from src.backend.core.pipeline_manager import PipelineManager
from src.backend.enums.model_type import ModelType
from src.backend.enums.step_type import StepType
from src.backend.prediction_manager import PredictionManager
from src.backend.registry import create_step
from src.frontend.pyqt_frontend import PyQtFrontend


def _config(name: StepType, args):
    if name is StepType.IMAGE_LOADER:
        model_type = ModelType(args.model) if args.model else None
        return ImageLoaderConfig(source_path=args.source, output_path=args.output, model_type=model_type)
    elif name is StepType.ANNOTATE:
        model_type = ModelType(args.model) if args.model else None
        ssh = SSHConfig(
            host=args.ssh_host or "",
            port=args.ssh_port,
            user=args.ssh_user or "",
            key_path=args.ssh_key_path or "",
            remote_work_dir=args.remote_work_dir,
            remote_model_path=args.remote_model_path or "",
            remote_python=args.remote_python,
        ) if args.ssh_host else None
        return AnnotateStepConfig(model_type=model_type, model_path=args.model_path, ssh=ssh)


def run(args) -> None:
    steps = [StepType(s) for s in args.steps]

    app = QApplication(sys.argv)

    if steps == [StepType.SELECT]:
        manager = PredictionManager(args.output)
    else:
        has_frontend = steps[-1] is StepType.SELECT
        pipeline_names = steps[:-1] if has_frontend else steps

        source_step = None
        step_instances = []
        for i, name in enumerate(pipeline_names):
            instance = create_step(name, _config(name, args))
            if i == 0:
                source_step = instance
            else:
                step_instances.append(instance)

        manager = PipelineManager(source_step, step_instances, workspace=args.output,
                                  with_frontend=has_frontend)
        manager.start()

    window = PyQtFrontend(manager)
    window.show()
    app.exec()

import sys

from PyQt6.QtWidgets import QApplication

from src.backend.config.annotate_step_config import AnnotateStepConfig
from src.backend.config.image_loader_config import ImageLoaderConfig
from src.backend.config.ssh_config import SSHConfig
from src.backend.enums.model_type import ModelType
from src.backend.enums.step_type import StepType
from src.backend.pipeline_engine.pipeline_manager import PipelineManager
from src.backend.pipeline_engine.registry import StepRegistry
from src.frontend_open.pyqt.pyqt_frontend import PyQtFrontend


class Runner:
    def __init__(self, args):
        self.args = args
        self.manager = None

    def run(self) -> None:
        self.start_pipeline()
        if self._has_frontend:
            app = QApplication(sys.argv)
            window = PyQtFrontend(self.manager)
            window.show()
            app.exec()
        else:
            self.manager.wait()

    def start_pipeline(self) -> None:
        steps = [StepType(s) for s in self.args.steps]

        if steps == [StepType.SELECT]:
            self.manager = PipelineManager(
                source_step=None,
                pipeline_steps=[],
                workspace=self.args.output,
                with_frontend=True,
                only_pending=self.args.only_pending,
            )
            self._has_frontend = True
        else:
            self._has_frontend = steps[-1] == StepType.SELECT
            pipeline_names = steps[:-1] if self._has_frontend else steps

            source_step = None
            step_instances = []
            for i, name in enumerate(pipeline_names):
                instance = StepRegistry.create_step(name, self._build_config(name))
                if i == 0:
                    source_step = instance
                else:
                    step_instances.append(instance)

            self.manager = PipelineManager(
                source_step,
                step_instances,
                workspace=self.args.output,
                with_frontend=self._has_frontend,
            )

        self.manager.start()

    def _build_config(self, name: StepType):
        if name == StepType.LOAD:
            model_type = ModelType(self.args.model) if self.args.model else None
            return ImageLoaderConfig(
                source_path=self.args.source,
                output_path=self.args.output,
                model_type=model_type,
            )
        elif name == StepType.ANNOTATE:
            model_type = ModelType(self.args.model) if self.args.model else None
            ssh = (
                SSHConfig(
                    host=self.args.ssh_host or '',
                    port=self.args.ssh_port,
                    user=self.args.ssh_user or '',
                    key_path=self.args.ssh_key_path or '',
                    remote_work_dir=self.args.remote_work_dir,
                    remote_model_path=self.args.remote_model_path or '',
                    remote_python=self.args.remote_python,
                    inference_script=self.args.inference_script or '',
                    force_credentials=getattr(self.args, 'force_ssh_credentials', False),
                )
                if self.args.ssh_host
                else None
            )
            return AnnotateStepConfig(
                model_type=model_type,
                model_path=self.args.model_path,
                ssh=ssh,
            )

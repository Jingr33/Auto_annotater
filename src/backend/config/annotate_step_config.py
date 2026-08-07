from dataclasses import dataclass

from backend.config.ssh_config import SSHConfig
from backend.enums.model_type import ModelType


@dataclass
class AnnotateStepConfig:
    model_type: ModelType
    model_path: str = ""
    ssh: SSHConfig = None

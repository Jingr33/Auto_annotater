import os
from dataclasses import dataclass


@dataclass
class SSHConfig:
    host: str = ''
    port: int = 22
    user: str = ''
    key_path: str = ''
    remote_work_dir: str = '/tmp/medsam2'
    remote_model_path: str = ''
    remote_python: str = 'python3'
    inference_script: str = ''
    force_credentials: bool = False

    def __post_init__(self) -> None:
        self.remote_work_dir = self._restore_msys_path(self.remote_work_dir)
        self.remote_model_path = self._restore_msys_path(self.remote_model_path)
        self.remote_python = self._restore_msys_path(self.remote_python)

    @staticmethod
    def _restore_msys_path(path: str) -> str:
        if not os.environ.get('MSYSTEM'):
            return path
        normalized_path = path.replace('\\', '/')
        prefix = 'C:/Program Files/Git'
        if normalized_path == prefix:
            return '/'
        if normalized_path.startswith(f'{prefix}/'):
            return normalized_path[len(prefix) :]
        return path

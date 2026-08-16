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

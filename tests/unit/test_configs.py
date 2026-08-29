from backend.config.annotate_step_config import AnnotateStepConfig
from backend.config.image_loader_config import ImageLoaderConfig
from backend.config.ssh_config import SSHConfig
from backend.enums.model_type import ModelType


def test_image_loader_config_defaults() -> None:
    config = ImageLoaderConfig(source_path='/data', output_path='/output')
    assert config.source_path == '/data'
    assert config.output_path == '/output'
    assert config.model_type is None


def test_image_loader_config_with_model() -> None:
    config = ImageLoaderConfig(
        source_path='/data',
        output_path='/output',
        model_type=ModelType.YOLO,
    )
    assert config.model_type == ModelType.YOLO


def test_annotate_step_config_defaults() -> None:
    config = AnnotateStepConfig(model_type=ModelType.YOLO)
    assert config.model_type == ModelType.YOLO
    assert config.model_path == ''
    assert config.ssh is None


def test_annotate_step_config_with_path() -> None:
    config = AnnotateStepConfig(
        model_type=ModelType.YOLO,
        model_path='/models/yolo.pt',
    )
    assert config.model_path == '/models/yolo.pt'


def test_ssh_config_defaults() -> None:
    config = SSHConfig()
    assert config.host == ''
    assert config.port == 22
    assert config.user == ''
    assert config.key_path == ''
    assert config.remote_work_dir == '/tmp/medsam2'
    assert config.remote_model_path == ''
    assert config.remote_python == 'python3'
    assert config.inference_script == ''
    assert config.force_credentials is False


def test_ssh_config_custom() -> None:
    config = SSHConfig(
        host='example.com',
        port=2222,
        user='admin',
        key_path='/path/to/key',
        remote_work_dir='/work',
        remote_model_path='/model.pt',
        remote_python='python3.10',
        inference_script='/scripts/run.py',
        force_credentials=True,
    )
    assert config.host == 'example.com'
    assert config.port == 2222
    assert config.user == 'admin'
    assert config.key_path == '/path/to/key'
    assert config.remote_work_dir == '/work'
    assert config.remote_model_path == '/model.pt'
    assert config.remote_python == 'python3.10'
    assert config.inference_script == '/scripts/run.py'
    assert config.force_credentials is True

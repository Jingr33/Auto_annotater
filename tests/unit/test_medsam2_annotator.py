from pathlib import Path
from unittest.mock import MagicMock

import pytest

from backend.annotators.medsam2_annotator import MedSAM2Annotator
from backend.config.ssh_config import SSHConfig
from backend.enums.run_mode import RunMode


def test_build_remote_script_uploads_local_model_when_remote_path_is_missing(tmp_path: Path) -> None:
    model_path = tmp_path / 'medsam2.pt'
    model_path.write_bytes(b'model')
    ssh = SSHConfig(host='example.com', remote_work_dir='/tmp/medsam2')
    remote = MagicMock()
    remote.remote_work_dir = '/tmp/medsam2'
    remote.remote_path.side_effect = lambda name: f'/tmp/medsam2/{name}'
    remote.upload_inference_script.return_value = '/tmp/medsam2/runner.py'
    remote.upload_file.return_value = '/tmp/medsam2/medsam2.pt'

    annotator = MedSAM2Annotator(
        model_path=str(model_path),
        run=RunMode.REMOTE,
        ssh=ssh,
    )
    annotator._remote = remote

    command = annotator._build_remote_script('/tmp/medsam2/image.jpg', None)

    assert command.startswith("export MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*'; cd ")
    assert '--model /tmp/medsam2/medsam2.pt' in command
    remote.upload_file.assert_called_once_with(str(model_path), 'medsam2.pt')


def test_build_remote_script_requires_a_model_path(tmp_path: Path) -> None:
    ssh = SSHConfig(host='example.com', remote_work_dir='/tmp/medsam2')
    remote = MagicMock()
    remote.remote_work_dir = '/tmp/medsam2'
    annotator = MedSAM2Annotator(
        model_path=str(tmp_path / 'missing.pt'),
        run=RunMode.REMOTE,
        ssh=ssh,
    )
    annotator._remote = remote

    with pytest.raises(RuntimeError, match='remote model is not configured'):
        annotator._build_remote_script('/tmp/medsam2/image.jpg', None)


def test_default_runner_uploads_default_remote_script() -> None:
    ssh = SSHConfig(host='example.com', remote_work_dir='/tmp/medsam2')
    remote = MagicMock()
    remote.remote_work_dir = '/tmp/medsam2'
    remote.remote_path.side_effect = lambda name: f'/tmp/medsam2/{name}'
    remote.upload_inference_script.return_value = '/tmp/medsam2/medsam2_remote_inference_default.py'
    annotator = MedSAM2Annotator(run=RunMode.REMOTE, ssh=ssh)
    annotator._remote = remote

    runner = annotator._ensure_remote_runner()

    assert runner == '/tmp/medsam2/medsam2_remote_inference_default.py'
    remote.upload_inference_script.assert_called_once()
    assert remote.upload_inference_script.call_args.args[1] == 'medsam2_remote_inference_default.py'


def test_custom_runner_is_uploaded_using_its_filename(tmp_path: Path) -> None:
    custom_runner = tmp_path / 'custom_runner.py'
    custom_runner.write_text("print('runner')", encoding='utf-8')
    ssh = SSHConfig(
        host='example.com',
        remote_work_dir='/tmp/medsam2',
        inference_script=str(custom_runner),
    )
    remote = MagicMock()
    remote.remote_work_dir = '/tmp/medsam2'
    remote.upload_inference_script.return_value = '/tmp/medsam2/custom_runner.py'
    annotator = MedSAM2Annotator(run=RunMode.REMOTE, ssh=ssh)
    annotator._remote = remote

    runner = annotator._ensure_remote_runner()

    assert runner == '/tmp/medsam2/custom_runner.py'
    remote.upload_inference_script.assert_called_once_with(str(custom_runner), 'custom_runner.py')

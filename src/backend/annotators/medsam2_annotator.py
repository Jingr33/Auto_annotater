import json
import os
import posixpath
import shlex
import tempfile

from backend.annotations.polygon_annotation import PolygonAnnotation
from backend.annotators.base_annotator import BaseAnnotator
from backend.config.medsam2_config import MedSAM2Config
from backend.config.ssh_config import SSHConfig
from backend.credentials_management.windows_credential_manager import WindowsCredentialManager
from backend.enums.run_mode import RunMode
from backend.remote.ssh_transport import SSHTransport


class MedSAM2Annotator(BaseAnnotator):
    def __init__(
        self,
        model_path: str = None,
        run: RunMode = RunMode.REMOTE,
        ssh: SSHConfig = None,
    ):
        self.model_path = model_path or MedSAM2Config.MODEL_PATH
        self.run = run
        self.ssh = ssh or SSHConfig()
        self._transport: SSHTransport | None = None
        self._remote_runner_path: str | None = None

    def annotate(self, image_path: str) -> list[PolygonAnnotation]:
        remote_img = self._transfer_image(image_path)
        self._run_prediction(remote_img)
        result_file = self._fetch_result(remote_img)
        return self._parse_mask_result(result_file)

    def annotate_with_bbox(self, image_path: str, bbox: tuple[float, float, float, float]) -> list[PolygonAnnotation]:
        remote_img = self._transfer_image(image_path)
        self._run_prediction(remote_img, bbox=bbox)
        result_file = self._fetch_result(remote_img)
        return self._parse_mask_result(result_file)

    def cleanup(self) -> None:
        if self._transport is not None:
            self._transport.close()
            self._transport = None
        self._remote_runner_path = None
        tmp = self._local_tmp_dir
        if os.path.isdir(tmp):
            for f in os.listdir(tmp):
                os.remove(os.path.join(tmp, f))

    @property
    def _local_tmp_dir(self) -> str:
        d = os.path.join(tempfile.gettempdir(), 'medsam2_tmp')
        os.makedirs(d, exist_ok=True)
        return d

    def _get_transport(self) -> SSHTransport:
        if self.run is not RunMode.REMOTE:
            raise RuntimeError('MedSAM2 local inference is not implemented')
        if self._transport is None:
            credentials = WindowsCredentialManager().get_or_prompt(
                host=self.ssh.host,
                port=self.ssh.port,
                username=self.ssh.user,
                force_prompt=self.ssh.force_credentials,
            )
            self._transport = SSHTransport(self.ssh, credentials)
        return self._transport

    def _transfer_image(self, local_path: str) -> str:
        filename = os.path.basename(local_path)
        remote_path = posixpath.join(self.ssh.remote_work_dir, filename)
        self._get_transport().put(local_path, remote_path)
        return remote_path

    def _ensure_remote_runner(self) -> str:
        if self._remote_runner_path is None:
            if self.ssh.inference_script:
                local_runner = os.path.abspath(self.ssh.inference_script)
            else:
                local_runner = os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        '..',
                        '..',
                        '..',
                        'scripts',
                        'medsam2_remote_inference.py',
                    )
                )
            remote_runner = posixpath.join(
                self.ssh.remote_work_dir,
                'auto_annotater_medsam2_inference.py',
            )
            self._get_transport().put(local_runner, remote_runner)
            self._remote_runner_path = remote_runner
        return self._remote_runner_path

    def _run_prediction(
        self,
        remote_image_path: str,
        bbox: tuple[float, float, float, float] | None = None,
    ) -> None:
        script = self._build_remote_script(remote_image_path, bbox)
        self._get_transport().run(script)

    def _build_remote_script(
        self,
        remote_image_path: str,
        bbox: tuple[float, float, float, float] | None,
    ) -> str:
        output_path = remote_image_path.rsplit('.', 1)[0] + '_result.json'
        bbox_value = bbox or (0.5, 0.5, 1.0, 1.0)
        bbox_argument = ','.join(str(value) for value in bbox_value)
        runner = self._ensure_remote_runner()
        base_model = posixpath.join(self.ssh.remote_work_dir, 'medsam_vit_b.pth')
        model = self.ssh.remote_model_path
        command = [
            self.ssh.remote_python,
            runner,
            '--image',
            remote_image_path,
            '--result',
            output_path,
            '--base-model',
            base_model,
            '--model',
            model,
            '--bbox',
            bbox_argument,
        ]
        return f'cd {shlex.quote(self.ssh.remote_work_dir)} && {shlex.join(command)}'

    def _fetch_result(self, remote_image_path: str) -> str:
        result_name = os.path.basename(remote_image_path).rsplit('.', 1)[0] + '_result.json'
        remote_path = posixpath.join(self.ssh.remote_work_dir, result_name)
        local_path = os.path.join(self._local_tmp_dir, result_name)
        self._get_transport().get(remote_path, local_path)
        return local_path

    def _parse_mask_result(self, result_file: str) -> list[PolygonAnnotation]:
        if not os.path.exists(result_file):
            return []
        with open(result_file, encoding='utf-8') as f:
            data = json.load(f)
        annotations = []
        for poly_data in data.get('polygons', []):
            points = [(p[0], p[1]) for p in poly_data['points']]
            annotations.append(
                PolygonAnnotation(
                    class_index=poly_data.get('class_index', 0),
                    points=points,
                )
            )
        return annotations

import json
import os
import subprocess
import tempfile
from typing import List, Optional, Tuple

from backend.annotations.polygon_annotation import PolygonAnnotation
from backend.annotators.base_annotator import BaseAnnotator
from backend.config.medsam2_config import MedSAM2Config
from backend.config.ssh_config import SSHConfig
from backend.enums.run_mode import RunMode


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

    def annotate(self, image_path: str) -> List[PolygonAnnotation]:
        remote_img = self._transfer_image(image_path)
        self._run_prediction(remote_img, mode="auto")
        result_file = self._fetch_result(remote_img)
        return self._parse_mask_result(result_file)

    def annotate_with_bbox(
        self, image_path: str, bbox: Tuple[float, float, float, float]
    ) -> List[PolygonAnnotation]:
        remote_img = self._transfer_image(image_path)
        self._run_prediction(remote_img, mode="bbox", bbox=bbox)
        result_file = self._fetch_result(remote_img)
        return self._parse_mask_result(result_file)

    def annotate_with_point(
        self, image_path: str, point: Tuple[float, float]
    ) -> List[PolygonAnnotation]:
        remote_img = self._transfer_image(image_path)
        self._run_prediction(remote_img, mode="point", point=point)
        result_file = self._fetch_result(remote_img)
        return self._parse_mask_result(result_file)

    def cleanup(self) -> None:
        tmp = self._local_tmp_dir
        if os.path.isdir(tmp):
            for f in os.listdir(tmp):
                os.remove(os.path.join(tmp, f))

    @property
    def _local_tmp_dir(self) -> str:
        d = os.path.join(tempfile.gettempdir(), "medsam2_tmp")
        os.makedirs(d, exist_ok=True)
        return d

    def _ssh_cmd(self, script: str) -> List[str]:
        cmd = ["ssh"]
        if self.ssh.key_path:
            cmd += ["-i", self.ssh.key_path]
        cmd += ["-p", str(self.ssh.port), f"{self.ssh.user}@{self.ssh.host}", script]
        return cmd

    def _scp_cmd(self, src: str, dst: str) -> List[str]:
        cmd = ["scp"]
        if self.ssh.key_path:
            cmd += ["-i", self.ssh.key_path]
        cmd += ["-P", str(self.ssh.port), src, dst]
        return cmd

    def _transfer_image(self, local_path: str) -> str:
        filename = os.path.basename(local_path)
        remote_path = os.path.join(self.ssh.remote_work_dir, filename)
        subprocess.run(
            self._scp_cmd(local_path, f"{self.ssh.user}@{self.ssh.host}:{remote_path}"),
            check=True,
        )
        return remote_path

    def _run_prediction(
        self,
        remote_image_path: str,
        mode: str = "auto",
        bbox: Optional[Tuple[float, float, float, float]] = None,
        point: Optional[Tuple[float, float]] = None,
    ) -> None:
        script = self._build_remote_script(remote_image_path, mode, bbox, point)
        subprocess.run(self._ssh_cmd(script), check=True)

    def _build_remote_script(
        self,
        remote_image_path: str,
        mode: str,
        bbox: Optional[Tuple[float, float, float, float]],
        point: Optional[Tuple[float, float]],
    ) -> str:
        output_path = remote_image_path.rsplit(".", 1)[0] + "_result.json"
        python = self.ssh.remote_python
        return f"cd {self.ssh.remote_work_dir} && {python} -c 'import json; result={{\"polygons\": []}}; open(\"{output_path}\", \"w\").write(json.dumps(result))'"

    def _fetch_result(self, remote_image_path: str) -> str:
        result_name = os.path.basename(remote_image_path).rsplit(".", 1)[0] + "_result.json"
        remote_path = os.path.join(self.ssh.remote_work_dir, result_name)
        local_path = os.path.join(self._local_tmp_dir, result_name)
        subprocess.run(
            self._scp_cmd(f"{self.ssh.user}@{self.ssh.host}:{remote_path}", local_path),
            check=True,
        )
        return local_path

    def _parse_mask_result(self, result_file: str) -> List[PolygonAnnotation]:
        if not os.path.exists(result_file):
            return []
        with open(result_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        annotations = []
        for poly_data in data.get("polygons", []):
            points = [(p[0], p[1]) for p in poly_data["points"]]
            annotations.append(
                PolygonAnnotation(
                    class_index=poly_data.get("class_index", 0),
                    points=points,
                )
            )
        return annotations

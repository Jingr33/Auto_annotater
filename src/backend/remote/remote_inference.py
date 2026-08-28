import os
import posixpath

from src.backend.config.ssh_config import SSHConfig
from src.backend.credentials_management.windows_credential_manager import WindowsCredentialManager
from src.backend.remote.remote_connection_error import RemoteConnectionError
from src.backend.remote.ssh_transport import SSHTransport


class RemoteInference:
    def __init__(
        self,
        config: SSHConfig,
        credential_manager: WindowsCredentialManager | None = None,
    ) -> None:
        self.config = config
        self._credential_manager = credential_manager
        self._transport: SSHTransport | None = None
        self._uploaded_scripts: dict[tuple[str, str], str] = {}

    def upload_file(self, local_path: str, remote_name: str | None = None) -> str:
        name = remote_name or os.path.basename(local_path)
        remote_path = self.remote_path(name)
        self._get_transport().put(local_path, remote_path)
        return remote_path

    def upload_inference_script(self, local_path: str, remote_name: str) -> str:
        key = (local_path, remote_name)
        if key not in self._uploaded_scripts:
            self._uploaded_scripts[key] = self.upload_file(local_path, remote_name)
        return self._uploaded_scripts[key]

    def download_file(self, remote_path: str, local_path: str) -> str:
        self._get_transport().get(remote_path, local_path)
        return local_path

    def run(self, command: str) -> str:
        return self._get_transport().run(command)

    def remote_path(self, name: str) -> str:
        return posixpath.join(self.config.remote_work_dir, name)

    @property
    def remote_work_dir(self) -> str:
        return self.config.remote_work_dir

    def close(self) -> None:
        if self._transport is not None:
            self._transport.close()
            self._transport = None
        self._uploaded_scripts.clear()

    def _get_transport(self) -> SSHTransport:
        if self._transport is None:
            try:
                manager = self._credential_manager or WindowsCredentialManager()
                credentials = manager.get_or_prompt(
                    host=self.config.host,
                    port=self.config.port,
                    username=self.config.user,
                    force_prompt=self.config.force_credentials,
                )
                self._transport = SSHTransport(self.config, credentials)
            except Exception as error:
                raise RemoteConnectionError.for_server(
                    self.config.host,
                    self.config.port,
                    error,
                ) from None
        return self._transport

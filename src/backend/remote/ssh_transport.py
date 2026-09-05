import os

import paramiko

from backend.config.ssh_config import SSHConfig
from backend.credentials_management.ssh_credentials import SSHCredentials


class SSHTransport:
    def __init__(self, config: SSHConfig, credentials: SSHCredentials) -> None:
        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()
        self._client.set_missing_host_key_policy(paramiko.RejectPolicy())
        self._client.connect(
            hostname=config.host,
            port=config.port,
            username=credentials.username,
            password=credentials.password,
            key_filename=config.key_path or None,
            look_for_keys=not bool(config.key_path),
            allow_agent=True,
            timeout=30,
        )

    def put(self, local_path: str, remote_path: str) -> None:
        with self._client.open_sftp() as sftp:
            self._ensure_remote_dir(sftp, os.path.dirname(remote_path))
            sftp.put(local_path, remote_path)

    def _ensure_remote_dir(self, sftp: paramiko.SFTPClient, remote_dir: str) -> None:
        if not remote_dir:
            return
        try:
            sftp.stat(remote_dir)
        except FileNotFoundError:
            self._ensure_remote_dir(sftp, os.path.dirname(remote_dir))
            sftp.mkdir(remote_dir)

    def get(self, remote_path: str, local_path: str) -> None:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with self._client.open_sftp() as sftp:
            sftp.get(remote_path, local_path)

    def run(self, command: str) -> str:
        _, stdout, stderr = self._client.exec_command(command, environment={'MSYS_NO_PATHCONV': '1'})
        exit_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if exit_code != 0:
            details = '\n'.join(part for part in (error.strip(), output.strip()) if part)
            if not details:
                details = 'No output was returned by the remote command.'
            raise RuntimeError(f'Remote command failed with exit code {exit_code}: {details}\nCommand: {command}')
        return output

    def close(self) -> None:
        self._client.close()

from unittest.mock import MagicMock

import pytest

from backend.remote.ssh_transport import SSHTransport


def test_run_includes_remote_output_when_stderr_is_empty() -> None:
    stdout = MagicMock()
    stdout.channel.recv_exit_status.return_value = 1
    stdout.read.return_value = b'process terminated without writing to stderr'
    stderr = MagicMock()
    stderr.read.return_value = b''
    client = MagicMock()
    client.exec_command.return_value = (None, stdout, stderr)
    transport = SSHTransport.__new__(SSHTransport)
    transport._client = client

    with pytest.raises(RuntimeError, match='process terminated without writing to stderr'):
        transport.run('python3 runner.py')

    client.exec_command.assert_called_once_with(
        'python3 runner.py',
        environment={'MSYS_NO_PATHCONV': '1'},
    )

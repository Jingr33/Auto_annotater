from dataclasses import dataclass


@dataclass(frozen=True)
class SSHCredentials:
    username: str
    password: str

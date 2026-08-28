from src.backend.errors.user_facing_error import UserFacingError


class RemoteConnectionError(UserFacingError):
    @classmethod
    def for_server(cls, host: str, port: int, error: Exception) -> 'RemoteConnectionError':
        message = (
            f'Cannot connect to remote server {host}:{port}. '
            'Check that the server is reachable and SSH credentials are correct.\n'
            f'Details: {error}'
        )
        return cls(message)

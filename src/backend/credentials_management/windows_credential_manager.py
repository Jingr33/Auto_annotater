import ctypes
import os
from ctypes import wintypes

from backend.credentials_management._credential import _Credential
from backend.credentials_management._credential_ui_info import _CredentialUIInfo
from backend.credentials_management.credential_constants import (
    CRED_PERSIST_LOCAL_MACHINE,
    CRED_TYPE_GENERIC,
    CREDUI_FLAGS_ALWAYS_SHOW_UI,
    CREDUI_FLAGS_GENERIC_CREDENTIALS,
    CREDUI_FLAGS_SHOW_SAVE_CHECK_BOX,
    ERROR_CANCELLED,
    ERROR_NOT_FOUND,
)
from backend.credentials_management.ssh_credentials import SSHCredentials


class WindowsCredentialManager:
    _target_prefix = "AutoAnnotater/SSH"

    def __init__(self) -> None:
        if os.name != "nt":
            raise OSError("Windows Credential Manager is available only on Windows")
        self._advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
        self._credui = ctypes.WinDLL("credui", use_last_error=True)
        self._configure_api()

    def get_or_prompt(
        self,
        host: str,
        port: int,
        username: str,
        force_prompt: bool = False,
    ) -> SSHCredentials:
        target = self._target(host, port, username)
        if not force_prompt:
            stored = self._read(target)
            if stored is not None:
                return stored
        return self._prompt(target, username)

    def delete(self, host: str, port: int, username: str) -> None:
        target = self._target(host, port, username)
        self._advapi32.CredDeleteW(target, CRED_TYPE_GENERIC, 0)

    def _target(self, host: str, port: int, username: str) -> str:
        return f"{self._target_prefix}/{host}:{port}/{username}"

    def _configure_api(self) -> None:
        self._advapi32.CredReadW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.POINTER(ctypes.POINTER(_Credential)),
        ]
        self._advapi32.CredReadW.restype = wintypes.BOOL
        self._advapi32.CredWriteW.argtypes = [
            ctypes.POINTER(_Credential),
            wintypes.DWORD,
        ]
        self._advapi32.CredWriteW.restype = wintypes.BOOL
        self._advapi32.CredFree.argtypes = [ctypes.c_void_p]
        self._advapi32.CredFree.restype = None
        self._credui.CredUIPromptForCredentialsW.argtypes = [
            ctypes.POINTER(_CredentialUIInfo),
            wintypes.LPCWSTR,
            ctypes.c_void_p,
            wintypes.DWORD,
            wintypes.LPWSTR,
            wintypes.DWORD,
            wintypes.LPWSTR,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.BOOL),
            wintypes.DWORD,
        ]
        self._credui.CredUIPromptForCredentialsW.restype = wintypes.DWORD

    def _read(self, target: str) -> SSHCredentials | None:
        credential = ctypes.POINTER(_Credential)()
        result = self._advapi32.CredReadW(
            target,
            CRED_TYPE_GENERIC,
            0,
            ctypes.byref(credential),
        )
        if not result:
            error = ctypes.get_last_error()
            if error == ERROR_NOT_FOUND:
                return None
            raise ctypes.WinError(error)

        try:
            value = credential.contents
            password_bytes = ctypes.string_at(
                value.credential_blob,
                value.credential_blob_size,
            )
            return SSHCredentials(
                username=value.user_name or "",
                password=password_bytes.decode("utf-8"),
            )
        finally:
            self._advapi32.CredFree(credential)

    def _prompt(self, target: str, username: str) -> SSHCredentials:
        username_buffer = ctypes.create_unicode_buffer(username, 513)
        password_buffer = ctypes.create_unicode_buffer("", 513)
        save = wintypes.BOOL(True)
        info = _CredentialUIInfo(
            cb_size=ctypes.sizeof(_CredentialUIInfo),
            parent=None,
            message="Enter SSH credentials for Auto-Annotater.",
            caption="Auto-Annotater SSH credentials",
            banner=None,
        )
        flags = (
            CREDUI_FLAGS_ALWAYS_SHOW_UI
            | CREDUI_FLAGS_GENERIC_CREDENTIALS
            | CREDUI_FLAGS_SHOW_SAVE_CHECK_BOX
        )
        result = self._credui.CredUIPromptForCredentialsW(
            ctypes.byref(info),
            target,
            None,
            0,
            username_buffer,
            len(username_buffer),
            password_buffer,
            len(password_buffer),
            ctypes.byref(save),
            flags,
        )
        if result == ERROR_CANCELLED:
            raise PermissionError("SSH credential prompt was cancelled")
        if result != 0:
            raise ctypes.WinError(result)

        credentials = SSHCredentials(
            username=username_buffer.value,
            password=password_buffer.value,
        )
        user_target = f"{target.rsplit('/', 1)[0]}/{credentials.username}"
        self._write(user_target, credentials)
        return credentials

    def _write(self, target: str, credentials: SSHCredentials) -> None:
        password_buffer = ctypes.create_string_buffer(
            credentials.password.encode("utf-8")
        )
        credential = _Credential(
            credential_type=CRED_TYPE_GENERIC,
            target_name=target,
            credential_blob_size=len(password_buffer.raw) - 1,
            credential_blob=ctypes.cast(
                password_buffer,
                ctypes.POINTER(ctypes.c_ubyte),
            ),
            persist=CRED_PERSIST_LOCAL_MACHINE,
            user_name=credentials.username,
        )
        if not self._advapi32.CredWriteW(ctypes.byref(credential), 0):
            raise ctypes.WinError(ctypes.get_last_error())

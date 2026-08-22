import ctypes
from ctypes import wintypes


class _CredentialUIInfo(ctypes.Structure):
    _fields_ = [
        ("cb_size", wintypes.DWORD),
        ("parent", wintypes.HWND),
        ("message", wintypes.LPWSTR),
        ("caption", wintypes.LPWSTR),
        ("banner", wintypes.HBITMAP),
    ]

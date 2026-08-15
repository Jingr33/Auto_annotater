from dataclasses import dataclass
from datetime import datetime


@dataclass
class LicenseStatusResponseDTO:
    valid: bool
    features: list[str]
    expires_at: str | None
    email: str | None


@dataclass
class LicenseActivateResponseDTO:
    valid: bool
    features: list[str]
    error: str | None

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class LicenseError(Exception):
    pass


class Feature(Enum):
    PRO = "pro"
    API = "api"
    REACT_UI = "react_ui"
    ADVANCED_ANNOTATION = "advanced_annotation"


@dataclass
class LicenseStatus:
    valid: bool
    features: list[Feature]
    expires_at: datetime | None = None
    email: str | None = None
    token: str | None = None


@dataclass
class LicenseValidationResult:
    valid: bool
    license_status: LicenseStatus | None = None
    error: str | None = None

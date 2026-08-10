from dataclasses import dataclass

from backend.license.models.license_status import LicenseStatus


@dataclass
class LicenseValidationResult:
    valid: bool
    license_status: LicenseStatus | None = None
    error: str | None = None

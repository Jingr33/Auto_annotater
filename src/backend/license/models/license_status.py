from dataclasses import dataclass
from datetime import datetime

from backend.license.models.feature import Feature


@dataclass
class LicenseStatus:
    valid: bool
    features: list[Feature]
    expires_at: datetime | None = None
    email: str | None = None
    token: str | None = None

from abc import ABC, abstractmethod

from backend.license.models import LicenseStatus, LicenseValidationResult


class LicenseProvider(ABC):
    @abstractmethod
    def validate_token(self, token: str) -> LicenseValidationResult:
        pass

    @abstractmethod
    def get_current_status(self) -> LicenseStatus:
        pass

    @abstractmethod
    def activate(self, token: str) -> LicenseValidationResult:
        pass

from abc import ABC, abstractmethod

from backend.license.models import LicenseValidationResult


class LicenseProvider(ABC):
    @abstractmethod
    def validate_token(self, token: str) -> LicenseValidationResult:
        pass

    @abstractmethod
    def activate(self, token: str) -> LicenseValidationResult:
        pass

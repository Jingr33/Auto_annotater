import json
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.license.models import Feature, LicenseStatus, LicenseValidationResult
from backend.license.provider import LicenseProvider

logger = logging.getLogger(__name__)


class LicenseManager:
    _instance = None
    _LICENSE_FILE = Path.home() / ".auto_annotater" / "license.json"

    def __init__(self):
        self._provider = self._create_provider()
        self._current_status: LicenseStatus | None = None
        self._load_saved_license()

    @classmethod
    def get_instance(cls) -> "LicenseManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _create_provider(self) -> LicenseProvider:
        provider_type = os.getenv("LICENSE_PROVIDER", "jwt")

        if provider_type == "jwt":
            from backend.license.validators.jwt_validator import JWTValidator

            return JWTValidator()
        elif provider_type == "server":
            from backend.license.validators.server_validator import ServerValidator

            return ServerValidator()
        else:
            raise ValueError(f"Unknown license provider: {provider_type}")

    def _load_saved_license(self) -> None:
        if self._LICENSE_FILE.exists():
            try:
                data = json.loads(self._LICENSE_FILE.read_text())
                token = data.get("token")
                if token:
                    result = self._provider.validate_token(token)
                    if result.valid:
                        self._current_status = result.license_status
                        logger.info(
                            "Loaded saved license for: %s",
                            result.license_status.email,
                        )
            except Exception as e:
                logger.warning("Failed to load saved license: %s", e)

    def _save_license(self, token: str) -> None:
        self._LICENSE_FILE.parent.mkdir(parents=True, exist_ok=True)
        self._LICENSE_FILE.write_text(json.dumps({"token": token}))
        logger.info("License saved to: %s", self._LICENSE_FILE)

    def validate(self, token: str) -> LicenseValidationResult:
        logger.info("Validating license token...")
        result = self._provider.validate_token(token)

        if result.valid:
            self._current_status = result.license_status
            self._save_license(token)
            logger.info("License valid for: %s", result.license_status.email)
        else:
            logger.warning("License validation failed: %s", result.error)

        return result

    def has_feature(self, feature: Feature) -> bool:
        if self._current_status is None:
            return False
        return feature in self._current_status.features

    def get_status(self) -> LicenseStatus:
        if self._current_status is None:
            return LicenseStatus(valid=False, features=[])
        return self._current_status

    def activate(self, token: str) -> LicenseValidationResult:
        return self.validate(token)

    def deactivate(self) -> None:
        self._current_status = None
        if self._LICENSE_FILE.exists():
            self._LICENSE_FILE.unlink()
        logger.info("License deactivated")

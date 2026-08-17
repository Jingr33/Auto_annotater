import logging
import os
from datetime import datetime, timedelta

from license_config import PRO_LICENSE
from backend.license.models import Feature, LicenseStatus, LicenseValidationResult
from backend.license.provider import LicenseProvider


class JWTValidator(LicenseProvider):
    def __init__(self, logger: logging.Logger | None = None):
        self._logger = logger or logging.getLogger(__name__)
        self._public_key = os.getenv("LICENSE_PUBLIC_KEY", "")

    def validate_token(self, token: str) -> LicenseValidationResult:
        try:
            self._logger.info("JWTValidator: Validating token...")

            if PRO_LICENSE:
                self._logger.info("JWTValidator: PRO_LICENSE=True, returning valid")
                return LicenseValidationResult(
                    valid=True,
                    license_status=LicenseStatus(
                        valid=True,
                        features=[
                            Feature.PRO,
                            Feature.API,
                            Feature.REACT_UI,
                            Feature.ADVANCED_ANNOTATION,
                        ],
                        expires_at=datetime.now() + timedelta(days=365),
                        email="licensed@auto-annotater.local",
                        token=token,
                    ),
                )
            else:
                self._logger.info("JWTValidator: PRO_LICENSE=False, returning invalid")
                return LicenseValidationResult(
                    valid=False,
                    error="No valid license (PRO_LICENSE=False)",
                )

        except Exception as e:
            self._logger.error("JWTValidator: Validation error: %s", e)
            return LicenseValidationResult(valid=False, error=str(e))

    def activate(self, token: str) -> LicenseValidationResult:
        return self.validate_token(token)

    def get_current_status(self) -> LicenseStatus:
        if PRO_LICENSE:
            return LicenseStatus(
                valid=True,
                features=[
                    Feature.PRO,
                    Feature.API,
                    Feature.REACT_UI,
                    Feature.ADVANCED_ANNOTATION,
                ],
                email="licensed@auto-annotater.local",
            )
        return LicenseStatus(valid=False, features=[])

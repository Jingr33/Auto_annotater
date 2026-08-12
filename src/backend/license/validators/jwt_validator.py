import logging
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from license_config import PRO_LICENSE
from backend.license.models import Feature, LicenseStatus, LicenseValidationResult
from backend.license.provider import LicenseProvider

logger = logging.getLogger(__name__)


class JWTValidator(LicenseProvider):
    def __init__(self):
        self._public_key = os.getenv("LICENSE_PUBLIC_KEY", "")

    def validate_token(self, token: str) -> LicenseValidationResult:
        try:
            logger.info("JWTValidator: Validating token...")

            if PRO_LICENSE:
                logger.info("JWTValidator: PRO_LICENSE=True, returning valid")
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
                logger.info("JWTValidator: PRO_LICENSE=False, returning invalid")
                return LicenseValidationResult(
                    valid=False,
                    error="No valid license (PRO_LICENSE=False)",
                )

        except Exception as e:
            logger.error("JWTValidator: Validation error: %s", e)
            return LicenseValidationResult(valid=False, error=str(e))

    def activate(self, token: str) -> LicenseValidationResult:
        return self.validate_token(token)

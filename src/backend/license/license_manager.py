import json
import logging
import os

from backend.config.license_config import LICENSE_FILE_PATH
from backend.license.models import Feature, LicenseStatus, LicenseValidationResult
from backend.license.provider import LicenseProvider
from backend.license.validators.jwt_validator import JWTValidator
from backend.license.validators.server_validator import ServerValidator


class LicenseManager:
    _instance = None

    def __init__(self):
        self._provider = self._create_provider()
        self._current_status: LicenseStatus | None = None
        self._logger = logging.getLogger(__name__)
        self._load_saved_license()

    @classmethod
    def get_instance(cls) -> 'LicenseManager':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _create_provider(self) -> LicenseProvider:
        provider_type = os.getenv('LICENSE_PROVIDER', 'jwt')

        if provider_type == 'jwt':
            return JWTValidator()
        elif provider_type == 'server':
            return ServerValidator()
        else:
            raise ValueError(f'Unknown license provider: {provider_type}')

    def _load_saved_license(self) -> None:
        if LICENSE_FILE_PATH.exists():
            try:
                data = json.loads(LICENSE_FILE_PATH.read_text())
                token = data.get('token')
                if token:
                    result = self._provider.validate_token(token)
                    if result.valid:
                        self._current_status = result.license_status
                        self._logger.info(
                            'Loaded saved license for: %s',
                            result.license_status.email,
                        )
            except Exception as e:
                self._logger.warning('Failed to load saved license: %s', e)

    def _save_license(self, token: str) -> None:
        LICENSE_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        LICENSE_FILE_PATH.write_text(json.dumps({'token': token}))
        self._logger.info('License saved to: %s', LICENSE_FILE_PATH)

    def validate(self, token: str) -> LicenseValidationResult:
        self._logger.info('Validating license token...')
        result = self._provider.validate_token(token)

        if result.valid:
            self._current_status = result.license_status
            self._save_license(token)
            self._logger.info('License valid for: %s', result.license_status.email)
        else:
            self._logger.warning('License validation failed: %s', result.error)

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

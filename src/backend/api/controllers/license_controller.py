from backend.license.license_manager import LicenseManager


class LicenseController:
    _instance = None

    def __init__(self, license_manager: LicenseManager | None = None):
        self._license_manager = license_manager

    @classmethod
    def get_instance(cls) -> "LicenseController":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def initialize(cls, license_manager: LicenseManager) -> None:
        cls._instance = cls(license_manager)

    def get_license_status(self) -> dict:
        manager = self._get_license_manager()
        status = manager.get_status()
        return {
            "valid": status.valid,
            "features": [f.value for f in status.features],
            "expires_at": status.expires_at.isoformat() if status.expires_at else None,
            "email": status.email,
        }

    def activate_license(self, token: str) -> dict:
        manager = self._get_license_manager()
        result = manager.activate(token)
        return {
            "valid": result.valid,
            "features": (
                [f.value for f in result.license_status.features]
                if result.license_status
                else []
            ),
            "error": result.error,
        }

    def _get_license_manager(self) -> LicenseManager:
        if self._license_manager is None:
            self._license_manager = LicenseManager.get_instance()
        return self._license_manager

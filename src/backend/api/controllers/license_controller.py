from backend.license.license_manager import LicenseManager
from backend.api.dto.license_dto import LicenseStatusResponseDTO, LicenseActivateResponseDTO


class LicenseController:
    def __init__(self, license_manager: LicenseManager | None = None):
        self._license_manager = license_manager

    def set_license_manager(self, license_manager: LicenseManager) -> None:
        self._license_manager = license_manager

    def get_license_status(self) -> LicenseStatusResponseDTO:
        manager = self._get_license_manager()
        status = manager.get_status()
        return LicenseStatusResponseDTO(
            valid=status.valid,
            features=[f.value for f in status.features],
            expires_at=status.expires_at.isoformat() if status.expires_at else None,
            email=status.email,
        )

    def activate_license(self, token: str) -> LicenseActivateResponseDTO:
        manager = self._get_license_manager()
        result = manager.activate(token)
        return LicenseActivateResponseDTO(
            valid=result.valid,
            features=(
                [f.value for f in result.license_status.features]
                if result.license_status
                else []
            ),
            error=result.error,
        )

    def _get_license_manager(self) -> LicenseManager:
        if self._license_manager is None:
            self._license_manager = LicenseManager.get_instance()
        return self._license_manager

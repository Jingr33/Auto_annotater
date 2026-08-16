from fastapi import APIRouter

from backend.api.dto.license_activate_request import LicenseActivateRequest
from backend.api.dto.license_dto import LicenseActivateResponseDTO, LicenseStatusResponseDTO
from backend.license.license_manager import LicenseManager


class LicenseController:
    def __init__(self, license_manager: LicenseManager):
        self._license_manager = license_manager
        self._router = APIRouter()
        self._setup_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _setup_routes(self) -> None:
        self._router.get('/license/status')(self.get_license_status)
        self._router.post('/license/activate')(self.activate_license)

    def get_license_status(self) -> LicenseStatusResponseDTO:
        status = self._license_manager.get_status()
        return LicenseStatusResponseDTO(
            valid=status.valid,
            features=[f.value for f in status.features],
            expires_at=status.expires_at.isoformat() if status.expires_at else None,
            email=status.email,
        )

    def activate_license(self, request: LicenseActivateRequest) -> LicenseActivateResponseDTO:
        result = self._license_manager.activate(request.token)
        return LicenseActivateResponseDTO(
            valid=result.valid,
            features=([f.value for f in result.license_status.features] if result.license_status else []),
            error=result.error,
        )

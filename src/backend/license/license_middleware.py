import logging

from dataclasses import asdict

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from backend.license.license_manager import LicenseManager
from backend.license.models import LicenseErrorResponse


class LicenseMiddleware(BaseHTTPMiddleware):
    EXEMPT_PATHS = [
        "/api/license/status",
        "/api/license/activate",
        "/docs",
        "/openapi.json",
    ]

    def __init__(self, app):
        super().__init__(app)
        self._logger = logging.getLogger(__name__)

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)

        license_token = request.headers.get("X-License-Token")

        if not license_token:
            self._logger.warning("No license token provided for: %s", request.url.path)
            return JSONResponse(
                status_code=401,
                content=asdict(LicenseErrorResponse(detail="License token required")),
            )

        manager = LicenseManager.get_instance()
        result = manager.validate(license_token)

        if not result.valid:
            self._logger.warning("Invalid license token for: %s", request.url.path)
            return JSONResponse(
                status_code=403,
                content=asdict(LicenseErrorResponse(detail="Invalid license token")),
            )

        request.state.license = result.license_status

        return await call_next(request)

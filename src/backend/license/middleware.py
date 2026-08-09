import logging

from fastapi import Request
from fastapi.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class LicenseMiddleware(BaseHTTPMiddleware):
    EXEMPT_PATHS = [
        "/api/license/status",
        "/api/license/activate",
        "/docs",
        "/openapi.json",
    ]

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)

        license_token = request.headers.get("X-License-Token")

        if not license_token:
            logger.warning("No license token provided for: %s", request.url.path)
            return JSONResponse(
                status_code=401,
                content={"detail": "License token required"},
            )

        from backend.license.license_manager import LicenseManager

        manager = LicenseManager.get_instance()
        result = manager.validate(license_token)

        if not result.valid:
            logger.warning("Invalid license token for: %s", request.url.path)
            return JSONResponse(
                status_code=403,
                content={"detail": "Invalid license token"},
            )

        request.state.license = result.license_status

        return await call_next(request)

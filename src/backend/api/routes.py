import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.core.pipeline_manager import PipelineManager
from backend.license.license_manager import LicenseManager

router = APIRouter()


class LicenseActivateRequest(BaseModel):
    token: str


@router.get("/license/status")
async def get_license_status() -> dict:
    manager = LicenseManager.get_instance()
    status = manager.get_status()
    return {
        "valid": status.valid,
        "features": [f.value for f in status.features],
        "expires_at": status.expires_at.isoformat() if status.expires_at else None,
        "email": status.email,
    }


@router.post("/license/activate")
async def activate_license(request: LicenseActivateRequest) -> dict:
    manager = LicenseManager.get_instance()
    result = manager.activate(request.token)
    return {
        "valid": result.valid,
        "features": (
            [f.value for f in result.license_status.features]
            if result.license_status
            else []
        ),
        "error": result.error,
    }

_manager: PipelineManager | None = None


def set_pipeline_manager(manager: PipelineManager) -> None:
    global _manager
    _manager = manager


def _get_manager() -> PipelineManager:
    if _manager is None:
        raise HTTPException(status_code=503, detail="PipelineManager not initialized")
    return _manager


@router.get("/items")
async def get_items() -> dict:
    manager = _get_manager()
    items = manager.data_manager.get_items()
    return {"items": items, "total": len(items)}


@router.get("/items/{item_id}/image")
async def get_item_image(item_id: str) -> dict:
    manager = _get_manager()
    path = manager.data_manager.image_path(item_id)
    return {"url": f"/api/items/{item_id}/image/file"}


@router.get("/items/{item_id}/image/file")
async def get_item_image_file(item_id: str) -> FileResponse:
    manager = _get_manager()
    path = manager.data_manager.image_path(item_id)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(path, media_type="image/jpeg")


@router.get("/pipeline/status")
async def get_pipeline_status() -> dict:
    manager = _get_manager()
    current = manager.get_current()
    return {
        "is_waiting": manager.is_waiting(),
        "is_finished": manager.is_finished(),
        "total": manager.get_total(),
        "current_item_id": current.item_id if current else None,
    }


@router.post("/pipeline/accept")
async def accept_item() -> dict:
    manager = _get_manager()
    manager.accept()
    return {"success": True}


@router.post("/pipeline/reject")
async def reject_item() -> dict:
    manager = _get_manager()
    manager.reject()
    return {"success": True}


@router.post("/pipeline/skip")
async def skip_item() -> dict:
    manager = _get_manager()
    manager.skip()
    return {"success": True}


@router.post("/pipeline/back")
async def go_back() -> dict:
    manager = _get_manager()
    success = manager.back()
    return {"success": success}

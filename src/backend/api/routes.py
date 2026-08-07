from fastapi import APIRouter
from fastapi.responses import FileResponse

from backend.core.pipeline_manager import PipelineManager

router = APIRouter()

_manager: PipelineManager | None = None


def set_pipeline_manager(manager: PipelineManager) -> None:
    global _manager
    _manager = manager


def _get_manager() -> PipelineManager:
    if _manager is None:
        raise RuntimeError("PipelineManager not initialized")
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

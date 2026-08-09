import os

from fastapi import HTTPException
from fastapi.responses import FileResponse

from backend.core.pipeline_manager import PipelineManager


class PipelineController:
    def __init__(self, manager: PipelineManager | None = None):
        self._manager = manager

    def set_manager(self, manager: PipelineManager) -> None:
        self._manager = manager

    def _get_manager(self) -> PipelineManager:
        if self._manager is None:
            raise HTTPException(status_code=503, detail="PipelineManager not initialized")
        return self._manager

    def get_items(self) -> dict:
        manager = self._get_manager()
        items = manager.data_manager.get_items()
        return {"items": items, "total": len(items)}

    def get_item_image(self, item_id: str) -> dict:
        manager = self._get_manager()
        path = manager.data_manager.image_path(item_id)
        return {"url": f"/api/items/{item_id}/image/file"}

    def get_item_image_file(self, item_id: str) -> FileResponse:
        manager = self._get_manager()
        path = manager.data_manager.image_path(item_id)
        if not os.path.isfile(path):
            raise HTTPException(status_code=404, detail="Image not found")
        return FileResponse(path, media_type="image/jpeg")

    def get_pipeline_status(self) -> dict:
        manager = self._get_manager()
        current = manager.get_current()
        return {
            "is_waiting": manager.is_waiting(),
            "is_finished": manager.is_finished(),
            "total": manager.get_total(),
            "current_item_id": current.item_id if current else None,
        }

    def accept_item(self) -> dict:
        manager = self._get_manager()
        manager.accept()
        return {"success": True}

    def reject_item(self) -> dict:
        manager = self._get_manager()
        manager.reject()
        return {"success": True}

    def skip_item(self) -> dict:
        manager = self._get_manager()
        manager.skip()
        return {"success": True}

    def go_back(self) -> dict:
        manager = self._get_manager()
        success = manager.back()
        return {"success": success}

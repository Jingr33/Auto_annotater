import os

from fastapi import HTTPException
from fastapi.responses import FileResponse

from backend.core.pipeline_manager import PipelineManager
from backend.api.dto.item_dto import ItemDTO, ItemListResponseDTO
from backend.api.dto.image_dto import ImageUrlResponseDTO
from backend.api.dto.pipeline_dto import PipelineStatusResponseDTO
from backend.api.dto.action_dto import ActionResultDTO


class PipelineController:
    def __init__(self, manager: PipelineManager | None = None):
        self._manager = manager

    def set_manager(self, manager: PipelineManager) -> None:
        self._manager = manager

    def _get_manager(self) -> PipelineManager:
        if self._manager is None:
            raise HTTPException(status_code=503, detail="PipelineManager not initialized")
        return self._manager

    def get_items(self) -> ItemListResponseDTO:
        manager = self._get_manager()
        items = manager.data_manager.get_items()
        item_dtos = [
            ItemDTO(
                id=item["id"],
                status=item["status"],
                created_at=item["created_at"],
                updated_at=item["updated_at"],
            )
            for item in items
        ]
        return ItemListResponseDTO(items=item_dtos, total=len(items))

    def get_item_image(self, item_id: str) -> ImageUrlResponseDTO:
        manager = self._get_manager()
        path = manager.data_manager.image_path(item_id)
        return ImageUrlResponseDTO(url=f"/api/items/{item_id}/image/file")

    def get_item_image_file(self, item_id: str) -> FileResponse:
        manager = self._get_manager()
        path = manager.data_manager.image_path(item_id)
        if not os.path.isfile(path):
            raise HTTPException(status_code=404, detail="Image not found")
        return FileResponse(path, media_type="image/jpeg")

    def get_pipeline_status(self) -> PipelineStatusResponseDTO:
        manager = self._get_manager()
        current = manager.get_current()
        return PipelineStatusResponseDTO(
            is_waiting=manager.is_waiting(),
            is_finished=manager.is_finished(),
            total=manager.get_total(),
            current_item_id=current.item_id if current else None,
        )

    def accept_item(self) -> ActionResultDTO:
        manager = self._get_manager()
        manager.accept()
        return ActionResultDTO(success=True)

    def reject_item(self) -> ActionResultDTO:
        manager = self._get_manager()
        manager.reject()
        return ActionResultDTO(success=True)

    def skip_item(self) -> ActionResultDTO:
        manager = self._get_manager()
        manager.skip()
        return ActionResultDTO(success=True)

    def go_back(self) -> ActionResultDTO:
        manager = self._get_manager()
        success = manager.back()
        return ActionResultDTO(success=success)

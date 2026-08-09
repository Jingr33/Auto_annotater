from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency_injector.wiring import Provide

from backend.api.containers import Container
from backend.api.controllers.pipeline_controller import PipelineController
from backend.api.controllers.license_controller import LicenseController
from backend.api.dto.item_dto import ItemListResponseDTO
from backend.api.dto.image_dto import ImageUrlResponseDTO
from backend.api.dto.pipeline_dto import PipelineStatusResponseDTO
from backend.api.dto.action_dto import ActionResultDTO
from backend.api.dto.license_dto import LicenseStatusResponseDTO, LicenseActivateResponseDTO

router = APIRouter()


class LicenseActivateRequest(BaseModel):
    token: str


@router.get("/items")
async def get_items(
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> ItemListResponseDTO:
    return controller.get_items()


@router.get("/items/{item_id}/image")
async def get_item_image(
    item_id: str,
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> ImageUrlResponseDTO:
    return controller.get_item_image(item_id)


@router.get("/items/{item_id}/image/file")
async def get_item_image_file(
    item_id: str,
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
):
    return controller.get_item_image_file(item_id)


@router.get("/pipeline/status")
async def get_pipeline_status(
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> PipelineStatusResponseDTO:
    return controller.get_pipeline_status()


@router.post("/pipeline/accept")
async def accept_item(
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> ActionResultDTO:
    return controller.accept_item()


@router.post("/pipeline/reject")
async def reject_item(
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> ActionResultDTO:
    return controller.reject_item()


@router.post("/pipeline/skip")
async def skip_item(
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> ActionResultDTO:
    return controller.skip_item()


@router.post("/pipeline/back")
async def go_back(
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> ActionResultDTO:
    return controller.go_back()


@router.get("/license/status")
async def get_license_status(
    controller: LicenseController = Depends(Provide[Container.license_controller]),
) -> LicenseStatusResponseDTO:
    return controller.get_license_status()


@router.post("/license/activate")
async def activate_license(
    request: LicenseActivateRequest,
    controller: LicenseController = Depends(Provide[Container.license_controller]),
) -> LicenseActivateResponseDTO:
    return controller.activate_license(request.token)

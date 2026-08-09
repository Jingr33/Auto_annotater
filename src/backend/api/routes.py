from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency_injector.wiring import Provide

from backend.api.containers import Container
from backend.api.controllers.pipeline_controller import PipelineController
from backend.api.controllers.license_controller import LicenseController

router = APIRouter()


class LicenseActivateRequest(BaseModel):
    token: str


@router.get("/items")
async def get_items(
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> dict:
    return controller.get_items()


@router.get("/items/{item_id}/image")
async def get_item_image(
    item_id: str,
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> dict:
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
) -> dict:
    return controller.get_pipeline_status()


@router.post("/pipeline/accept")
async def accept_item(
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> dict:
    return controller.accept_item()


@router.post("/pipeline/reject")
async def reject_item(
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> dict:
    return controller.reject_item()


@router.post("/pipeline/skip")
async def skip_item(
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> dict:
    return controller.skip_item()


@router.post("/pipeline/back")
async def go_back(
    controller: PipelineController = Depends(Provide[Container.pipeline_controller]),
) -> dict:
    return controller.go_back()


@router.get("/license/status")
async def get_license_status(
    controller: LicenseController = Depends(Provide[Container.license_controller]),
) -> dict:
    return controller.get_license_status()


@router.post("/license/activate")
async def activate_license(
    request: LicenseActivateRequest,
    controller: LicenseController = Depends(Provide[Container.license_controller]),
) -> dict:
    return controller.activate_license(request.token)

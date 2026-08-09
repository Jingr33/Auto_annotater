from fastapi import APIRouter
from pydantic import BaseModel

from backend.api.controllers.pipeline_controller import PipelineController
from backend.api.controllers.license_controller import LicenseController

router = APIRouter()


class LicenseActivateRequest(BaseModel):
    token: str


@router.get("/items")
async def get_items() -> dict:
    return PipelineController.get_instance().get_items()


@router.get("/items/{item_id}/image")
async def get_item_image(item_id: str) -> dict:
    return PipelineController.get_instance().get_item_image(item_id)


@router.get("/items/{item_id}/image/file")
async def get_item_image_file(item_id: str):
    return PipelineController.get_instance().get_item_image_file(item_id)


@router.get("/pipeline/status")
async def get_pipeline_status() -> dict:
    return PipelineController.get_instance().get_pipeline_status()


@router.post("/pipeline/accept")
async def accept_item() -> dict:
    return PipelineController.get_instance().accept_item()


@router.post("/pipeline/reject")
async def reject_item() -> dict:
    return PipelineController.get_instance().reject_item()


@router.post("/pipeline/skip")
async def skip_item() -> dict:
    return PipelineController.get_instance().skip_item()


@router.post("/pipeline/back")
async def go_back() -> dict:
    return PipelineController.get_instance().go_back()


@router.get("/license/status")
async def get_license_status() -> dict:
    return LicenseController.get_instance().get_license_status()


@router.post("/license/activate")
async def activate_license(request: LicenseActivateRequest) -> dict:
    return LicenseController.get_instance().activate_license(request.token)

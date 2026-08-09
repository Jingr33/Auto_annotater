from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router
from backend.license.middleware import LicenseMiddleware

app = FastAPI(title="Auto Annotater API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-License-Token"],
)

app.add_middleware(LicenseMiddleware)

app.include_router(router, prefix="/api")


def initialize_controllers(pipeline_manager=None) -> None:
    from backend.api.controllers.pipeline_controller import PipelineController
    from backend.api.controllers.license_controller import LicenseController
    from backend.license.license_manager import LicenseManager

    PipelineController.initialize(pipeline_manager)
    LicenseController.initialize(LicenseManager.get_instance())

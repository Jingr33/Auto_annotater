from fastapi import FastAPI

from dependency_injector import containers, providers

from backend.api.controllers.pipeline_controller import PipelineController
from backend.api.controllers.license_controller import LicenseController
from backend.license.license_manager import LicenseManager


class Container(containers.DeclarativeContainer):
    pipeline_manager = providers.Object(None)
    license_manager = providers.Singleton(LicenseManager.get_instance)

    pipeline_controller = providers.Singleton(
        PipelineController, manager=pipeline_manager
    )
    license_controller = providers.Singleton(
        LicenseController, license_manager=license_manager
    )


def register_routes(app: FastAPI) -> None:
    container: Container = app.container
    pipeline_controller = container.pipeline_controller()
    license_controller = container.license_controller()

    app.include_router(pipeline_controller.router, prefix="/api")
    app.include_router(license_controller.router, prefix="/api")

from dependency_injector import containers, providers
from fastapi import FastAPI

from src.backend.api.controllers.pipeline_controller import PipelineController


class Container(containers.DeclarativeContainer):
    pipeline_manager = providers.Object(None)

    pipeline_controller = providers.Singleton(PipelineController, manager=pipeline_manager)


def register_routes(app: FastAPI) -> None:
    container: Container = app.container
    pipeline_controller = container.pipeline_controller()

    app.include_router(pipeline_controller.router, prefix='/api')

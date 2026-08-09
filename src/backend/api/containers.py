from dependency_injector import containers, providers

from backend.api.controllers.pipeline_controller import PipelineController
from backend.api.controllers.license_controller import LicenseController
from backend.license.license_manager import LicenseManager


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "backend.api.routes",
        ]
    )

    pipeline_controller = providers.Singleton(PipelineController)
    license_controller = providers.Singleton(LicenseController)
    license_manager = providers.Singleton(LicenseManager.get_instance)

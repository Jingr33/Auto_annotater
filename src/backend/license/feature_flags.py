from backend.license.license_manager import LicenseManager
from backend.license.models import Feature


class FeatureFlags:
    def __init__(self):
        self._manager = LicenseManager.get_instance()

    @property
    def has_pro(self) -> bool:
        return self._manager.has_feature(Feature.PRO)

    @property
    def has_api(self) -> bool:
        return self._manager.has_feature(Feature.API)

    @property
    def has_react_ui(self) -> bool:
        return self._manager.has_feature(Feature.REACT_UI)

    @property
    def has_advanced_annotation(self) -> bool:
        return self._manager.has_feature(Feature.ADVANCED_ANNOTATION)

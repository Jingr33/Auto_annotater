from functools import wraps

from backend.license.license_manager import LicenseManager
from backend.license.models import Feature


def requires_license(feature: Feature):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            manager = LicenseManager.get_instance()
            if not manager.has_feature(feature):
                return None
            return func(*args, **kwargs)

        return wrapper

    return decorator

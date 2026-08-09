from functools import wraps

from backend.license.models import Feature
from backend.license.license_manager import LicenseManager


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


def requires_license_async(feature: Feature):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            manager = LicenseManager.get_instance()
            if not manager.has_feature(feature):
                return None
            return await func(*args, **kwargs)

        return wrapper

    return decorator

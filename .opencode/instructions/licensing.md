# Licensing Rules

## Overview

- `variant: open` — No license required, basic features only
- `variant: pro` — Requires valid license, all features enabled

## Configuration

- `license_config.py` contains `PRO_LICENSE` boolean
- Set to `True` for pro features, `False` for open only
- Temporary file, remove when real licensing is implemented

## Implementation

- License classes are real, not mocked
- Validation functions use `PRO_LICENSE` config as result
- All validator results are logged

## Decorator Usage

```python
from backend.license.decorators import requires_license
from backend.license.models import Feature

@requires_license(Feature.PRO)
def my_pro_feature():
    pass
```

## Dev Items with `variant: pro`

1. Must use `@requires_license` decorator
2. Only available when license is valid
3. Implementation follows same coding standards

## UI Flow

1. User enters license token at startup
2. Token stored in localStorage
3. All HTTP requests include `X-License-Token` header
4. Backend validates token on every request
5. If token expires during use, UI is visible but HTTP requests fail
6. On 401/403, UI automatically redirects to login screen

## Switching to Real License

1. Update validator logic in `jwt_validator.py` or `server_validator.py`
2. Remove `license_config.py`
3. No other code changes needed

## API Endpoints

- `GET /api/license/status` — Get current license status
- `POST /api/license/activate` — Activate a new license token

## Features

| Feature | Description |
|---------|-------------|
| `pro` | Pro version features |
| `api` | API access |
| `react_ui` | React frontend |
| `advanced_annotation` | Advanced annotation models |

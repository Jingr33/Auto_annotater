from pydantic import BaseModel


class LicenseActivateRequest(BaseModel):
    token: str

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router
from backend.api.containers import Container
from backend.license.middleware import LicenseMiddleware


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(title="Auto Annotater API")
    app.container = container

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

    return app


app = create_app()

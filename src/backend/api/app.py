from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.api.containers import Container


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(title='Auto Annotater API')
    app.container = container

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:5173'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    return app


app = create_app()

"""pytest open interface package,easy to use"""

__version__ = '0.0.1'

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from pytestapi.api import router


def run(prefix=''):
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix=prefix)
    from .database import engine, Base
    Base.metadata.create_all(bind=engine)

    return app

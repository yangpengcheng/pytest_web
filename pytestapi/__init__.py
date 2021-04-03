"""pytest open interface package,easy to use"""

__version__ = '0.0.1'

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from pytestapi.api import jenkins, pytest_run, scheduler, user,auth


def run(prefix=''):
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(jenkins.router)
    # app.include_router(auth.router)
    # app.include_router(pytest_run.router)
    # app.include_router(scheduler.router)
    # app.include_router(user.router)

    from .database import engine, Base
    Base.metadata.create_all(bind=engine)

    return app


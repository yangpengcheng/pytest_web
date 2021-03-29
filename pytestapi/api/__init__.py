from fastapi import APIRouter

router = APIRouter()


def init():
    from pytestapi.api.user import router
    from pytestapi.api.pytest_run import router
    from pytestapi.api.scheduler import router


init()

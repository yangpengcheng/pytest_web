from fastapi import APIRouter

router = APIRouter()


def init():
    from pytestapi.api.user import router
    from pytestapi.api.pytest_run import router
    from pytestapi.api.scheduler import router
    from pytestapi.api.jenkins import router


init()

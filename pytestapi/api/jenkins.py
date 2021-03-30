from pytestapi.api import router


@router.post("/jenkins/run")
async def create_job():
    pass

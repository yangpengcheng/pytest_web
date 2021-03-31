from starlette import status

from pytestapi.api import router
from pytestapi.config import JENKINS_URL, JENKINS_USERNAME, JENKINS_PASSWORD
from pytestapi.forms.args import Object
from pytestapi.jenkins import Jenkins
from pytestapi.view_models.base import HTTPException


@router.post("/jenkins/job", tags=["新建jenkins任务"])
async def create_job(obj: Object):
    try:
        server = Jenkins(url=JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
        server.create_job_by_dict(obj.name, obj.val)
    except Exception as e:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args)
    else:
        return {"msg": "任务新建成功"}


@router.get("/jenkins/job", tags=["获取jenkins任务信息"])
async def get_job_info(name: str):
    try:
        server = Jenkins(url=JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
        info = server.get_job_info(name)
    except Exception as e:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args)
    else:
        return info


@router.delete("/jenkins/job", tags=["删除jenkins任务"])
async def delete_job(name: str):
    try:
        server = Jenkins(url=JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
        server.delete_job(name)
    except Exception as e:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args)



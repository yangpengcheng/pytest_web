import jenkins
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from pytestapi.config import JENKINS_URL, JENKINS_USERNAME, JENKINS_PASSWORD
from pytestapi.forms.args import Object, Name
from pytestapi.jenkins import Jenkins
from pytestapi.view_models.base import HTTPException

router = APIRouter(prefix="/jenkins", tags=['jenkins'])


def get_jenkins():
    try:
        server = Jenkins(url=JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
        server.timeout = 2
        server.get_whoami()
    except jenkins.TimeoutException:
        HTTPException(False)(status_code=status.HTTP_404_NOT_FOUND, detail='jenkins 连接超时')
    else:
        return server


@router.post('/job', description='新建任务')
async def create_job(obj: Object, server=Depends(get_jenkins)):
    try:
        server.create_job_by_dict(obj.name, obj.val)
    except jenkins.JenkinsException as e:
        HTTPException(False)(status_code=status.HTTP_409_CONFLICT, detail=e.args)
    except Exception as e:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args)
    else:
        return Response(status_code=status.HTTP_201_CREATED)


@router.get('/job', description='获取任务信息')
async def get_job_info(name: str, server=Depends(get_jenkins)):
    try:
        info = server.get_job_info(name)
    except jenkins.NotFoundException as e:
        HTTPException(False)(status_code=status.HTTP_404_NOT_FOUND, detail=e.args)
    except Exception as e:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args)
    else:
        return info


@router.delete('/job/{name}', description='删除任务')
async def delete_job(name: str, server=Depends(get_jenkins)):
    try:
        server.delete_job(name)
    except jenkins.NotFoundException as e:
        HTTPException(False)(status_code=status.HTTP_404_NOT_FOUND, detail=e.args)
    except Exception as e:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/job/{name}/build', description='构建任务')
async def build_job(name: str, server=Depends(get_jenkins)):
    try:
        server.build_job(name)
    except jenkins.NotFoundException as e:
        HTTPException(False)(status_code=status.HTTP_404_NOT_FOUND, detail=e.args)
    except Exception as e:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/job/{name}/last_build_info', description='获取最近一次构建信息')
async def get_last_build_info(name: str, server=Depends(get_jenkins)):
    try:
        last_build_number = server.get_job_info(name)['lastCompletedBuild']['number']
        build_info = server.get_build_info(name, last_build_number)
    except jenkins.NotFoundException as e:
        HTTPException(False)(status_code=status.HTTP_404_NOT_FOUND, detail=e.args)
    except TypeError:
        HTTPException(False)(status_code=status.HTTP_404_NOT_FOUND, detail='无构建历史')
    except Exception as e:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args)
    else:
        return build_info

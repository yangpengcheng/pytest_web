import time

from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.schedulers import SchedulerAlreadyRunningError, SchedulerNotRunningError
from starlette import status

from pytestapi.api import router
from pytestapi.forms.args import JobArg, ID
from pytestapi.scheduler import scheduler
from pytestapi.view_models.base import HTTPException
from pytestapi.view_models.job import JobView, JobCollection


@router.get("/schedule/jobs", tags=["获取调度任务"])
async def get_schedule_jobs(job_id=None):
    if job_id:
        job = scheduler.get_job(job_id, jobstore="default")
        HTTPException(job)(status_code=status.HTTP_400_BAD_REQUEST, detail="任务id不存在")
        return JobView(job)
    else:
        jobs = JobCollection()
        jobs.fill(scheduler.get_jobs())
        return jobs


@router.post("/schedule/start", tags=["开启任务调度器"])
async def start_schedule():
    try:
        scheduler.start(paused=False)
    except ConflictingIdError:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail="任务id冲突")
    except SchedulerAlreadyRunningError:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail="任务调度器已处于开启状态")
    else:
        return {'msg': '任务调度器开启成功'}


@router.post("/schedule/shutdown", tags=["关闭任务调度器,暂时不要使用"])
async def shutdown_schedule():
    try:
        scheduler.shutdown(wait=True)
    except SchedulerNotRunningError:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail="任务调度器已处于关闭状态")
    else:
        return {'msg': '任务调度器关闭成功'}


@router.post("/schedule/pause", tags=["暂停任务调度器"])
async def pause_schedule():
    try:
        scheduler.pause()
    except SchedulerNotRunningError:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail="任务调度器已处于关闭状态")
    else:
        return {'msg': '任务调度器暂停成功'}


@router.post("/schedule/resume", tags=["恢复任务调度器"])
async def resume_schedule():
    try:
        scheduler.resume()
    except SchedulerNotRunningError:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail="任务调度器已处于关闭状态")
    else:
        return {'msg': '任务调度器恢复成功'}


def send_email(command=None, announcer=None, subscriber=None):
    print(f'发布者:{announcer},订阅者:{subscriber},命令:{command}', time.time())


@router.post("/schedule/job", tags=["添加任务"])
async def add_job(jobarg: JobArg):
    job = scheduler.get_job(jobarg.id, jobstore="default")
    HTTPException(job, reverse=True)(status_code=status.HTTP_400_BAD_REQUEST, detail="任务id已存在，添加任务失败")
    params = {
        "command": jobarg.command,
        "announcer": jobarg.announcer,
        "subscriber": jobarg.subscriber
    }
    scheduler.add_job(func=send_email, id=jobarg.id, trigger=jobarg.trigger, seconds=5, kwargs=params)
    return {'msg': '任务添加成功'}


@router.post("/schedule/job/pause", tags=["暂停任务"])
async def pause_job(job_id: ID):
    job = scheduler.get_job(job_id.id, jobstore="default")
    HTTPException(job)(status_code=status.HTTP_400_BAD_REQUEST, detail="任务id不存在")
    scheduler.pause_job(job_id.id)
    return {'msg': '暂停任务成功'}


@router.post("/schedule/job/resume", tags=["恢复任务"])
async def resume_job(job_id: ID):
    job = scheduler.get_job(job_id.id, jobstore="default")
    HTTPException(job)(status_code=status.HTTP_400_BAD_REQUEST, detail="任务id不存在")
    scheduler.resume_job(job_id.id)
    return {'msg': '恢复任务成功'}


@router.post("/schedule/job/remove", tags=["删除任务"])
async def remove_job(job_id: ID):
    job = scheduler.get_job(job_id.id, jobstore="default")
    HTTPException(job)(status_code=status.HTTP_400_BAD_REQUEST, detail="任务id不存在")
    scheduler.remove_job(job_id.id)
    return {'msg': '删除任务成功'}

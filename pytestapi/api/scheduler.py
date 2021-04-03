import time

from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.schedulers import SchedulerAlreadyRunningError, SchedulerNotRunningError
from fastapi import APIRouter, status

from pytestapi.forms.args import JobArg, ID
from pytestapi.scheduler import scheduler
from pytestapi.view_models.base import HTTPException
from pytestapi.view_models.job import JobView, JobCollection

router = APIRouter(prefix='/schedule', tags=['任务调度'])


@router.get('/jobs', description='获取调度任务')
async def get_schedule_jobs(job_id=None):
    if job_id:
        job = scheduler.get_job(job_id, jobstore='default')
        HTTPException(job)(status_code=status.HTTP_400_BAD_REQUEST, detail='任务id不存在')
        return JobView(job)
    else:
        jobs = JobCollection()
        jobs.fill(scheduler.get_jobs())
        return jobs


@router.post('/start', description='开启任务调度')
async def start_schedule():
    try:
        scheduler.start(paused=False)
    except ConflictingIdError:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail='任务id冲突')
    except SchedulerAlreadyRunningError:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail='任务调度器已处于开启状态')
    else:
        return {'msg': '任务调度器开启成功'}


@router.post('/shutdown', description='关闭任务调度,暂时不要使用')
async def shutdown_schedule():
    try:
        scheduler.shutdown(wait=True)
    except SchedulerNotRunningError:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail='任务调度器已处于关闭状态')
    else:
        return {'msg': '任务调度器关闭成功'}


@router.post('/pause', description='暂停任务调度器')
async def pause_schedule():
    try:
        scheduler.pause()
    except SchedulerNotRunningError:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail='任务调度器已处于关闭状态')
    else:
        return {'msg': '任务调度器暂停成功'}


@router.post('/resume', description='恢复任务调度器')
async def resume_schedule():
    try:
        scheduler.resume()
    except SchedulerNotRunningError:
        HTTPException(False)(status_code=status.HTTP_400_BAD_REQUEST, detail='任务调度器已处于关闭状态')
    else:
        return {'msg': '任务调度器恢复成功'}


def send_email(command=None, announcer=None, subscriber=None):
    print(f'发布者:{announcer},订阅者:{subscriber},命令:{command}', time.time())


@router.post('/job', description='添加任务')
async def add_job(jobarg: JobArg):
    job = scheduler.get_job(jobarg.id, jobstore="default")
    HTTPException(job, reverse=True)(status_code=status.HTTP_400_BAD_REQUEST, detail='任务id已存在，添加任务失败')
    params = {
        "command": jobarg.command,
        "announcer": jobarg.announcer,
        "subscriber": jobarg.subscriber
    }
    if jobarg.trigger == 'date':
        scheduler.add_job(func=send_email, id=jobarg.id, trigger=jobarg.trigger, run_date=jobarg.run_date,
                          timezone=jobarg.timezone, kwargs=params)
    elif jobarg.trigger == 'cron':
        scheduler.add_job(func=send_email, id=jobarg.id, trigger=jobarg.trigger, year=jobarg.year,
                          month=jobarg.month, day=jobarg.day, week=jobarg.week, day_of_week=jobarg.day_of_week,
                          hour=jobarg.hour, minute=jobarg.minute, second=jobarg.second, start_date=jobarg.start_date,
                          end_date=jobarg.end_date, timezone=jobarg.timezone, jitter=jobarg.jitter, kwargs=params)
    else:
        scheduler.add_job(func=send_email, id=jobarg.id, trigger=jobarg.trigger, weeks=jobarg.weeks, days=jobarg.days,
                          hours=jobarg.hours, minutes=jobarg.minutes, seconds=jobarg.seconds,
                          start_date=jobarg.start_date, end_date=jobarg.end_date, timezone=jobarg.timezone,
                          jitter=jobarg.jitter, kwargs=params)
    return {'msg': '任务添加成功'}


@router.post('/job/pause', description='暂停任务')
async def pause_job(job_id: ID):
    job = scheduler.get_job(job_id.id, jobstore='default')
    HTTPException(job)(status_code=status.HTTP_400_BAD_REQUEST, detail='任务id不存在')
    scheduler.pause_job(job_id.id)
    return {'msg': '暂停任务成功'}


@router.post('/job/resume', description='恢复任务')
async def resume_job(job_id: ID):
    job = scheduler.get_job(job_id.id, jobstore='default')
    HTTPException(job)(status_code=status.HTTP_400_BAD_REQUEST, detail='任务id不存在')
    scheduler.resume_job(job_id.id)
    return {'msg': '恢复任务成功'}


@router.post('/job/remove', description='删除任务')
async def remove_job(job_id: ID):
    job = scheduler.get_job(job_id.id, jobstore='default')
    HTTPException(job)(status_code=status.HTTP_400_BAD_REQUEST, detail='任务id不存在')
    scheduler.remove_job(job_id.id)
    return {'msg': '删除任务成功'}

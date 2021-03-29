import pytz
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from pytestapi.config import SQLALCHEMY_DATABASE_URL

jobstores = {
    'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URL)
}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}


class Scheduler(BackgroundScheduler):
    def __init__(self):
        super(Scheduler, self).__init__(jobstores=jobstores, executors=executors, job_defaults=job_defaults,
                                        timezone=pytz.timezone('Asia/Shanghai'))


scheduler = Scheduler()


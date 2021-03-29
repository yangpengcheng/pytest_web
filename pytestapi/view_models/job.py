class JobView:
    def __init__(self, job):
        self.id = job.id
        self.func = job.func
        self.name = job.name
        self.executor = job.executor


class JobCollection:
    def __init__(self):
        self.total = 0
        self.jobs = []

    def fill(self, jobs, total=None):
        self.total = total or len(jobs)
        self.jobs = [JobView(job) for job in jobs]

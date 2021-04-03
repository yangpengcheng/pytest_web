import uvicorn
from fastapi import FastAPI

from pytestapi import run

# from pytestapi.config import JENKINS_USERNAME, JENKINS_URL, JENKINS_PASSWORD
# from pytestapi.jenkins import Jenkins

from pytestapi.api import jenkins, pytest_run, scheduler, user

app = run()


if __name__ == '__main__':
    uvicorn.run("run:app", host="127.0.0.1", port=5000, log_level="info", ssl_keyfile="localhost+2-key.pem",
                ssl_certfile="localhost+2.pem", reload=True)

    # server = Jenkins(url=JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
    # print(server.get_job_config_dict('pytest'))
    # server.create_job_by_dict('empty1')


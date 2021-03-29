import uvicorn

from pytestapi import run

app = run()


if __name__ == '__main__':
    uvicorn.run("run:app", host="127.0.0.1", port=5000, log_level="info", ssl_keyfile="localhost+2-key.pem",
                ssl_certfile="localhost+2.pem", reload=False)

    # server = jenkins.Jenkins('http://192.168.106.129:8080', username='admin', password='admin')

    # server = Jenkins('http://192.168.106.129:8080', 'admin', 'admin')
    # user = jenkins.server.get_whoami()
    # version = jenkins.server.get_version()
    # print('Hello %s from Jenkins %s' % (user['fullName'], version))

    # server.create_job('emoty')
    # server.build_job('emoty')
    # print(server.get_jobs()[0])

    # server.build_job('pytest')
    # last_build_number = server.get_job_info('pytest')['lastCompletedBuild']['number']
    # build_info = server.get_build_info('pytest', last_build_number)
    # print(build_info)
import uvicorn

from pytestapi import run

app = run()

if __name__ == '__main__':
    uvicorn.run("run:app", host="127.0.0.1", port=5000, log_level="info", ssl_keyfile="localhost+2-key.pem",
                ssl_certfile="localhost+2.pem", reload=False)

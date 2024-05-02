import uvicorn

from roslaunch_analyze_server.app import app


def run():
    uvicorn.run(app, host="localhost", port=8000)

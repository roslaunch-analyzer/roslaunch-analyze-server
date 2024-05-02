from fastapi import FastAPI

from roslaunch_analyze_server.launchfile_analyzer import get_required_arguments
from roslaunch_analyze_server.models import LaunchFile

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/analyze_required_arguments/")
async def analyze_required_arguments(launch_file: LaunchFile):
    return get_required_arguments(launch_file.path)

import logging
import os
from urllib.parse import unquote

import ament_index_python.packages
from fastapi import FastAPI

from roslaunch_analyze_server.launchfile_analyzer import get_required_arguments
from roslaunch_analyze_server.models import LaunchFile

app = FastAPI()


@app.get("/")
async def root():
    # return sample tree
    return {
        "name": "root",
        "children": [
            {
                "name": "child1",
                "children": [
                    {"name": "child1-1", "children": []},
                    {"name": "child1-2", "children": []},
                ],
            },
            {
                "name": "child2",
                "children": [
                    {"name": "child2-1", "children": []},
                    {"name": "child2-2", "children": []},
                ],
            },
        ],
    }


@app.get("/hello_world/")
async def hello_world():
    return "Hello, World!"


@app.get("/analyze_required_arguments/")
async def analyze_required_arguments(launch_file: LaunchFile):
    return get_required_arguments(launch_file.path)


@app.get("/data/")
async def data():
    import os
    import sys

    return {
        "current_dir": os.getcwd(),
        "python_path": sys.path,
        "PATH": os.environ.get("PATH"),
    }


@app.get("/get_package_share_directory/{package_name}")
async def get_package_share_directory(package_name: str):
    try:
        return ament_index_python.packages.get_package_share_directory(package_name)
    except ament_index_python.PackageNotFoundError:
        return f"Package {package_name} not found"


@app.get("/get_definition_of_file/{package_name}/{extra_path:path}")
async def get_definition_of_file(package_name: str, extra_path: str):
    extra_path = unquote(extra_path)
    logging.info(f"package_name: {package_name}, extra_path: {extra_path}")
    try:
        pkg_dir_path = ament_index_python.packages.get_package_share_directory(
            package_name
        )
    except ament_index_python.PackageNotFoundError:
        return f"Package {package_name} not found"

    file_path = pkg_dir_path + extra_path

    if not os.path.exists(file_path):
        return f"File {file_path} not found, pkg_dir_path: {pkg_dir_path}, extra_path: {extra_path}"

    file_path = os.path.realpath(file_path)

    return {
        "file_path": file_path,
    }

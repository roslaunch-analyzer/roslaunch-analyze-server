from typing import Any, Dict, List

from roslaunch_analyze_server.models import LaunchFile


def get_required_arguments(launch_file: LaunchFile) -> List[Dict[str, Any]]:
    # TODO: Implement this function
    return [
        {"name": "map_path", "default": None},
        {"name": "vehicle_model", "default": None},
        {"name": "sensor_model", "default": None},
        {"name": "pointcloud_container_name", "default": "pointcloud_container"},
    ]

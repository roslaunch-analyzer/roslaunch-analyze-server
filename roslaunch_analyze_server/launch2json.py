from pathlib import Path

from rclpy.logging import get_logger

from roslaunch_analyze_server.filter import filter_entity_tree
from roslaunch_analyze_server.parser import create_entity_tree
from roslaunch_analyze_server.serialization import make_entity_tree_serializable

logger = get_logger("launch2json")


def _parse_args():
    import argparse

    import rclpy
    from rclpy.node import Node
    from rclpy.parameter import Parameter
    from ros2launch.command.launch import LaunchCommand

    rclpy.init()

    node = Node("launch2json")
    node.declare_parameter("launch_command", Parameter.Type.STRING)

    launch_command = node.get_parameter("launch_command")
    argv = launch_command.value.replace("ros2 launch ", "").split(" ")

    # launch_command = "autoware_launch logging_simulator.launch.xml vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit map_path:=/home/ukenryu/autoware_map/rinkaifutoushin"
    # argv = launch_command.replace("ros2 launch ", "").split(" ")

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    LaunchCommand().add_arguments(parser, "ros2")

    rclpy.shutdown()

    return parser.parse_args(args=argv)

def _parse_dictionary(launch_file_path:str, launch_arguments:dict):
    import argparse
    import sys
    import rclpy
    from rclpy.node import Node
    from rclpy.parameter import Parameter
    from ros2launch.command.launch import LaunchCommand

    rclpy.init()

    node = Node("launch2json")
    node.declare_parameter("launch_command", Parameter.Type.STRING)

    # launch_command = "autoware_launch logging_simulator.launch.xml vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit map_path:=/home/ukenryu/autoware_map/rinkaifutoushin"
    launch_command = f"{launch_file_path} {' '.join([f'{k}:={v}' for k, v in launch_arguments.items()])}"
    argv = launch_command.replace("ros2 launch ", "").split(" ")
    print(argv)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    # LaunchCommand().add_arguments(parser, "ros2")
    parser.add_argument("launch_file_name", type=str, help="The launch file to be executed")
    parser.add_argument("launch_arguments", nargs="*", help="Arguments to pass to the launch file")
    parser.add_argument(
            '-n', '--noninteractive', default=not sys.stdin.isatty(), action='store_true',
            help='Run the launch system non-interactively, with no terminal associated')
    parser.add_argument(
        '-d', '--debug', default=False, action='store_true',
        help='Put the launch system in debug mode, provides more verbose output.')

    rclpy.shutdown()

    return parser.parse_args(args=argv)

def _prepare(args):
    import os
    import launch
    from ros2launch.api.api import get_share_file_path_from_package
    from ros2launch.api.api import parse_launch_arguments
    print(args)
    if os.path.exists(args.launch_file_name):
        launch_file_path = args.launch_file_name
    else:
        launch_file_path = get_share_file_path_from_package(
            package_name=args.package_name, file_name=args.launch_file_name
        )

    parsed_launch_arguments = parse_launch_arguments(args.launch_arguments)

    root_entity = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.AnyLaunchDescriptionSource(launch_file_path),
        launch_arguments=parsed_launch_arguments,
    )

    launch_service = launch.LaunchService(
        argv=parsed_launch_arguments, noninteractive=args.noninteractive, debug=args.debug
    )

    return root_entity, launch_service

def analyse_launch_path(launch_file_path: str, launch_arguments: dict)->dict:
    """ Main API for analysing a launch file and its arguments.
    """
    args = _parse_dictionary(launch_file_path, launch_arguments)
    root_entity, launch_service = _prepare(args)

    raw_tree = create_entity_tree(root_entity, launch_service)
    filtered_tree = filter_entity_tree(raw_tree.copy())
    serializable_tree = make_entity_tree_serializable(filtered_tree, launch_service.context)
    return serializable_tree

def main():
    """ main API for analysing a ros2 launch command.
    """
    import json

    args = _parse_args()
    root_entity, launch_service = _prepare(args)

    raw_tree = create_entity_tree(root_entity, launch_service)
    filtered_tree = filter_entity_tree(raw_tree.copy())
    serializable_tree = make_entity_tree_serializable(filtered_tree, launch_service.context)


    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)

    # tmp
    with open(output_dir / "entity_tree.json", "w") as f:
        json.dump(serializable_tree, f, indent=2)


if __name__ == "__main__":
    # main()
    launch_file_path = "/home/ukenryu/autoware/src/launcher/autoware_launch/autoware_launch/launch/logging_simulator.launch.xml"
    launch_arguments = {
        "vehicle_model": "sample_vehicle",
        "sensor_model": "sample_sensor_kit",
        "map_path": "/home/ukenryu/autoware_map/rinkaifutoushin",
    }
    serializable_tree = analyse_launch_path(launch_file_path, launch_arguments)
    import json
    with open("entity_tree.json", "w") as f:
        json.dump(serializable_tree, f, indent=2)

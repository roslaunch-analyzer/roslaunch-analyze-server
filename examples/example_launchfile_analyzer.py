#!/bin/python3

import json

from roslaunch_analyze_server.launch_tree import LaunchTree
from roslaunch_analyze_server.launchfile_analyzer import parse_xml


def main(
    launch_file: str,
    vehicle_model="sample_vehicle",
    sensor_model="sample_sensor_kit",
    **kwargs,
):
    # Start parsing from the main XML file
    context_tree = LaunchTree()
    context = dict()
    context["__tree__"] = context_tree

    # arguments
    context["vehicle_model"] = vehicle_model
    context["sensor_model"] = sensor_model
    for key in kwargs:
        context[key] = kwargs[key]
    context = parse_xml(launch_file, context=context)
    # print(context["__tree__"])
    json.dump(context["__tree__"].jsonify(), open("tree.json", "w"), indent=4)
    return context["__tree__"].jsonify()


if __name__ == "__main__":
    main(launch_file="path/to/launchfile.launch")

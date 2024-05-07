import xml.etree.ElementTree as ET

import yaml

from roslaunch_analyze_server.string_utils import analyze_string, find_linked_path


def read_ros_yaml(file_path: str) -> dict:
    """Read and return the contents of a YAML file."""
    with open(file_path, "r") as file:
        # Using safe_load() to avoid potential security risks
        data = yaml.safe_load(file)

    data = data["/**"]["ros__parameters"]
    return data


def parse_node_tag(
    node_tag: ET.Element, base_namespace: str, context: dict, local_context: dict
):
    pkg = analyze_string(node_tag.get("pkg"), context, local_context, base_namespace)
    exec = analyze_string(node_tag.get("exec"), context, local_context, base_namespace)
    local_parameters = {}
    local_parameters["__param_files"] = []
    # print(context, base_namespace)
    for child in node_tag:
        if child.tag == "param":
            if child.get("name") is not None:
                local_parameters[child.get("name")] = analyze_string(
                    child.get("value"), context, local_context, base_namespace
                )
            if child.get("from") is not None:
                path = analyze_string(
                    child.get("from"), context, local_context, base_namespace
                )
                path = find_linked_path(path)
                if path.endswith("_empty.param.yaml"):
                    continue
                print(path, child.get("from"))
                local_parameters["__param_files"].append(path)
                data = read_ros_yaml(path)
                for key in data:
                    if isinstance(data[key], str) and data[key].startswith("$(var "):
                        local_parameters[key] = analyze_string(
                            data[key], context, local_context, base_namespace
                        )
                    else:
                        local_parameters[key] = data[key]
    context["__tree__"].add_child(
        context["__current_launch_name_"], f"{pkg}/{exec}", **local_parameters
    )

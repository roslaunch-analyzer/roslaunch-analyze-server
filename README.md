<div align="center"><img src="icon.webp" height=200/></div>
<h1 align="center">🚀 ROS Launchfile Analyze Server 🚀</h1>

---

This package provides a tool to analyze ROS launchfiles. It is based on the [ros2/launch](https://github.com/ros2/launch) package and provides a server that can be used to analyze launchfiles. The server can be accessed via a REST API.

---

## Installation

```bash
pip install git+https://github.com/roslaunch-analyzer/roslaunch-analyze-server.git
```

or

```bash
pipx install git+https://github.com/roslaunch-analyzer/roslaunch-analyze-server.git
```

> [!NOTE]
> Make sure to have the [ROS2](https://docs.ros.org/en/humble/Installation.html) installed and `source /opt/ros/humble/setup.bash` is executed before entering the command.

### For Developers

1. This project uses [poetry](https://python-poetry.org/) for dependency management. First, you need to [install poetry](https://python-poetry.org/docs/#installation).
2. Clone the repository and navigate to the project directory.
3. Run `poetry install` to install the dependencies.

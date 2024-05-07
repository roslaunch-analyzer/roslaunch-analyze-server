# add python path
# It is temprarory solution to add python path. We need to find a better solution for this.
import sys

sys.path.extend(
    [
        "/opt/ros/humble/lib/python3.10/site-packages",
        "/opt/ros/humble/local/lib/python3.10/dist-packages",
    ]
)

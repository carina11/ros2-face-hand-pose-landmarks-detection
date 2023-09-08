import os

# ROS
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Generates LaunchDescription for face, hand, and pose detection."""
    param_file = os.path.join(
        get_package_share_directory(
            "face_hand_pose_detection"), "params", "face_hand_pose_detection.yaml"
    )

    face_hand_pose_detection = Node(
        name="face_hand_pose_detection_node",
        package="face_hand_pose_detection",
        executable="face_hand_pose_detection_node.py",
        emulate_tty=True,
        output={"both": {"screen", "log", "own_log"}},
        parameters=[
            param_file,
        ],
        arguments=["--ros-args", "--log-level", "info"],
    )

    nodes_list = [face_hand_pose_detection]

    return LaunchDescription(nodes_list)

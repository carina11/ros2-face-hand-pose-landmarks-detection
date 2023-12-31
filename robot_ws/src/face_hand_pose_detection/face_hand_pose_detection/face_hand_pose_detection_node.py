#!/usr/bin/env python3

from typing import List, Optional

# ROS
import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from rclpy.callback_groups import ReentrantCallbackGroup

# Thirdparty
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge

# ROS messages
from sensor_msgs.msg import Image

# Face, Hand, Pose Detection
from face_hand_pose_detection import FaceHandPoseDetection
from face_hand_pose_detection_msgs.msg import DetectionResult


class FaceHandPoseDetectionNode(Node):
    """This node detects faces, hands and human poses in the given image topic.

    Subscribes to an image.
    Publishes an image with results annotations.
    """

    def __init__(self) -> None:
        super().__init__("face_hand_pose_detection_node")

        # Read from parameters
        topic_image: str = self.declare_parameter(
            "topic_image", Parameter.Type.STRING).value

        qos = QoSProfile(depth=1, reliability=QoSReliabilityPolicy.BEST_EFFORT)

        self.create_subscription(
            Image,
            topic_image,
            callback=self._image_callback,
            qos_profile=qos,
            callback_group=ReentrantCallbackGroup()
        )

        self.bridge = CvBridge()
        self.face_hand_pose_detection = FaceHandPoseDetection()

        self._image_publisher = self.create_publisher(
            Image, "face_hand_pose_detection/image", 10)
        self._result_publisher = self.create_publisher(
            DetectionResult, "face_hand_pose_detection/result", 10)

    def _image_callback(self, image: Image) -> None:
        cv_image = self.bridge.imgmsg_to_cv2(image, "rgb8")
        result_image, detection_result = self.face_hand_pose_detection.detect(
            cv_image)
        self._result_publisher.publish(detection_result)
        self._image_publisher.publish(
            self.bridge.cv2_to_imgmsg(result_image, "rgb8"))


# pylint: disable=duplicate-code
def main(args: Optional[List[str]] = None) -> None:
    """Spins the face, hand, and pose detection node."""
    rclpy.init(args=args)
    node = FaceHandPoseDetectionNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

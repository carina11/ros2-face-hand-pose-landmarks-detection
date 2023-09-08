import mediapipe as mp
from ament_index_python.packages import get_package_share_directory
import os
import numpy as np
import cv2
from face_hand_pose_detection_msgs.msg import DetectionResult, Landmark


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic


class FaceHandPoseDetection:

    def __init__(self) -> None:
        
        # Load model
        self.model = mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            refine_face_landmarks=False
        )


    def detect(self, image: np.ndarray):
        """Runs Object Detection on the input image and returns an image with bounding box and results.

        Args:
            image (np.ndarra): Input image

        Returns:
            Image with landmarks
            Detection results
        """
        # Run the model
        results = self.model.process(image)

        # Convert to ROS messages
        detection_result = self._prepare_results(results)
        
        # Draw landmarks
        result_image = self.draw_result_landmarks(image, results)
        
        return result_image, detection_result


    @staticmethod
    def _prepare_results(results):
        detection_result = DetectionResult()
        
        if results.pose_landmarks:
            for pose in results.pose_landmarks.landmark:
                detection_result.pose_landmarks.append(
                    Landmark(
                        x=pose.x,
                        y=pose.y,
                        z=pose.z,
                        visibility=pose.visibility,
                    )
                )
        
        if results.pose_world_landmarks:
            for pose in results.pose_world_landmarks.landmark:
                detection_result.pose_world_landmarks.append(
                    Landmark(
                        x=pose.x,
                        y=pose.y,
                        z=pose.z,
                        visibility=pose.visibility,
                    )
                )
            
        if results.right_hand_landmarks:
            for hand in results.right_hand_landmarks.landmark:
                detection_result.right_hand_landmarks.append(
                    Landmark(
                        x=hand.x,
                        y=hand.y,
                        z=hand.z,
                    )
                )
            
        if results.left_hand_landmarks:
            for hand in results.left_hand_landmarks.landmark:
                detection_result.left_hand_landmarks.append(
                    Landmark(
                        x=hand.x,
                        y=hand.y,
                        z=hand.z,
                    )
                )
            
        if results.face_landmarks:
            for face in results.face_landmarks.landmark:
                detection_result.face_landmarks.append(
                    Landmark(
                        x=face.x,
                        y=face.y,
                        z=face.z,
                    )
                )
                
        return detection_result
        
        
    @staticmethod
    def draw_result_landmarks(image, results):
        mp_drawing.draw_landmarks(image, results.face_landmarks)
        mp_drawing.draw_landmarks(image, results.pose_landmarks)
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks)
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks)
        return image


import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceDetector:
    """
    Wraps MediaPipe's BlazeFace model. Job: given a frame, find face
    bounding boxes and draw them. Nothing else — no eyes, no head pose.
    """

    def __init__(self):
        model_path = "app/vision/models/blaze_face_short_range.tflite"

        base_options = python.BaseOptions(model_asset_path=model_path)

        options = vision.FaceDetectorOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            min_detection_confidence=0.6
        )

        self.detector = vision.FaceDetector.create_from_options(options)

    def detect(self, frame, mp_image):
        """
        Returns (detected: bool, face_count: int).
        Draws bounding boxes directly on `frame` as a side effect.
        """
        detection_result = self.detector.detect(mp_image)
        detected = bool(detection_result.detections)

        for detection in detection_result.detections:
            bbox = detection.bounding_box
            x, y = bbox.origin_x, bbox.origin_y
            width, height = bbox.width, bbox.height

            cv2.rectangle(
                frame,
                (x, y),
                (x + width, y + height),
                (0, 255, 0),
                2
            )

        return detected, len(detection_result.detections)
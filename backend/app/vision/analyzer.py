import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceAnalyzer:
    def __init__(self):

        model_path = "app/vision/models/blaze_face_short_range.tflite"

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.FaceDetectorOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            min_detection_confidence=0.6
        )

        self.detector = vision.FaceDetector.create_from_options(options)

    def analyze(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        detection_result = self.detector.detect(mp_image)

        detected = False

        if detection_result.detections:

            detected = True

            h, w, _ = frame.shape

            for detection in detection_result.detections:

                bbox = detection.bounding_box

                x = bbox.origin_x
                y = bbox.origin_y
                width = bbox.width
                height = bbox.height

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (0, 255, 0),
                    2,
                )

        return frame, detected
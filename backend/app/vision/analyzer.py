import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from app.vision.face_detector import FaceDetector
from app.vision.eye_tracker import EyeTracker
from app.vision.head_pose import HeadPose
from app.vision.confidence import ConfidenceScorer


class FaceAnalyzer:
    def __init__(self):
        self.face_detector = FaceDetector()
        self.eye_tracker = EyeTracker()
        self.head_pose = HeadPose()
        self.confidence_scorer = ConfidenceScorer()

        landmarker_options = vision.FaceLandmarkerOptions(
            base_options=python.BaseOptions(
                model_asset_path="app/vision/models/face_landmarker.task"
            ),
            running_mode=vision.RunningMode.IMAGE,
            num_faces=1
        )
        self.landmarker = vision.FaceLandmarker.create_from_options(
            landmarker_options
        )

    def analyze(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        detected, face_count = self.face_detector.detect(frame, mp_image)

        landmark_result = self.landmarker.detect(mp_image)
        landmarks = (
            landmark_result.face_landmarks[0]
            if landmark_result.face_landmarks
            else None
        )

        usable = detected and landmarks is not None

        eye_result = self.eye_tracker.analyze(landmarks)
        head_result = self.head_pose.analyze(landmarks)

        confidence_result = self.confidence_scorer.score(
            eye_result, head_result, detected
        )

        return frame, {
            "face_detected": usable,
            "faces": face_count,
            "attention_score": eye_result["attention_score"],
            "head_pose": head_result["head_pose"],
            "confidence_score": confidence_result["confidence_score"]
        }
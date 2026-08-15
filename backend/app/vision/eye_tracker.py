class EyeTracker:
    def __init__(self):
        self.previous_score = 50

    def analyze(self, landmarks):
        if landmarks is None:
            return {
                "eye_contact": False,
                "gaze_ratio": 0.5,
                "attention_score": 0
            }

        left_iris = landmarks[468]
        left_outer = landmarks[33]
        left_inner = landmarks[133]

        right_iris = landmarks[473]
        right_outer = landmarks[362]
        right_inner = landmarks[263]

        left_ratio = self._eye_ratio(left_iris, left_outer, left_inner)
        right_ratio = self._eye_ratio(right_iris, right_outer, right_inner)

        gaze_ratio = (left_ratio + right_ratio) / 2

        deviation = abs(gaze_ratio - 0.5)
        attention = 100 - int(deviation * 200)
        attention = max(0, min(100, attention))

        smooth_score = self.previous_score * 0.7 + attention * 0.3
        self.previous_score = smooth_score

        return {
            "eye_contact": smooth_score > 60,
            "gaze_ratio": round(gaze_ratio, 3),
            "attention_score": int(smooth_score)
        }

    def _eye_ratio(self, iris, outer_corner, inner_corner):
        eye_width = abs(outer_corner.x - inner_corner.x)
        if eye_width == 0:
            return 0.5

        iris_offset = abs(iris.x - inner_corner.x)
        return iris_offset / eye_width
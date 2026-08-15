class HeadPose:
    def analyze(self, landmarks):
        if landmarks is None:
            return {"head_pose": "No Face"}

        nose = landmarks[1]
        left_face = landmarks[454]
        right_face = landmarks[234]

        face_width = abs(left_face.x - right_face.x)
        if face_width == 0:
            return {"head_pose": "No Face"}

        nose_ratio = (nose.x - right_face.x) / face_width

        if nose_ratio < 0.40:
            pose = "Looking Right"
        elif nose_ratio > 0.60:
            pose = "Looking Left"
        else:
            pose = "Looking Center"

        return {"head_pose": pose}
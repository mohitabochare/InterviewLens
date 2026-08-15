import os
import joblib
import pandas as pd


MODEL_PATH = "app/vision/data/confidence_model.pkl"


class ConfidenceScorer:
    def __init__(self):
        self.model = None
        self.feature_cols = None

        if os.path.exists(MODEL_PATH):
            try:
                saved = joblib.load(MODEL_PATH)
                self.model = saved["model"]
                self.feature_cols = saved["feature_cols"]
                print("Confidence model loaded from training data.")
            except Exception as e:
                print(f"Could not load trained model, using fallback formula. ({e})")

    def score(self, eye_result, head_result, face_detected):
        if not face_detected:
            return {"confidence_score": 0}

        attention = eye_result["attention_score"]
        head_pose = head_result["head_pose"]

        if self.model is not None:
            return self._score_with_model(attention, head_pose)

        return self._score_with_formula(attention, head_pose)

    def _score_with_model(self, attention, head_pose):
        row = {col: 0 for col in self.feature_cols}
        row["attention_score"] = attention

        head_col = f"head_pose_{head_pose}"
        if head_col in row:
            row[head_col] = 1

        X = pd.DataFrame([row])[self.feature_cols]

        probabilities = self.model.predict_proba(X)[0]
        classes = list(self.model.classes_)
        attentive_index = classes.index("attentive")

        confidence = int(probabilities[attentive_index] * 100)
        return {"confidence_score": confidence}

    def _score_with_formula(self, attention, head_pose):
        head_centered = head_pose == "Looking Center"
        head_score = 100 if head_centered else 60

        confidence = int(attention * 0.6 + head_score * 0.4)
        confidence = max(0, min(100, confidence))

        return {"confidence_score": confidence}
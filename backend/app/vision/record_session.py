import csv
import os
import time

import cv2

from app.vision.analyzer import FaceAnalyzer


CSV_PATH = "app/vision/data/training_data.csv"


def ensure_csv_exists():
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "attention_score",
                "head_pose",
                "confidence_score",
                "label"
            ])


def record():
    ensure_csv_exists()

    cap = cv2.VideoCapture(0)
    analyzer = FaceAnalyzer()

    if not cap.isOpened():
        print("Error: Could not access camera.")
        return

    print("Hold 'A' = attentive, hold 'D' = distracted, 'Q' = quit.")

    logged_attentive = 0
    logged_distracted = 0

    with open(CSV_PATH, mode="a", newline="") as f:
        writer = csv.writer(f)

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            frame, result = analyzer.analyze(frame)

            key = cv2.waitKey(1) & 0xFF

            label = None
            if key == ord("a"):
                label = "attentive"
            elif key == ord("d"):
                label = "distracted"
            elif key == ord("q"):
                break

            if label and result["face_detected"] and result["head_pose"] != "No Face":
                writer.writerow([
                    time.time(),
                    result["attention_score"],
                    result["head_pose"],
                    result["confidence_score"],
                    label
                ])

                if label == "attentive":
                    logged_attentive += 1
                else:
                    logged_distracted += 1

            display_text = f"Label: {label or '...'}"
            color = (0, 255, 0) if label == "attentive" else (
                0, 0, 255) if label == "distracted" else (200, 200, 200)

            cv2.putText(
                frame, display_text, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2
            )
            cv2.putText(
                frame,
                f"Logged - attentive: {logged_attentive}  distracted: {logged_distracted}",
                (20, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1
            )

            cv2.imshow("InterviewLens Recorder", frame)

    cap.release()
    cv2.destroyAllWindows()

    print(f"Done. Logged {logged_attentive} attentive, {logged_distracted} distracted frames.")
    print(f"Saved to {CSV_PATH}")


if __name__ == "__main__":
    record()
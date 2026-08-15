import cv2
from app.vision.analyzer import FaceAnalyzer


def start_camera():

    cap = cv2.VideoCapture(0)

    analyzer = FaceAnalyzer()

    if not cap.isOpened():
        print("Error: Could not access camera.")
        return

    print("Press 'q' to quit.")

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame.")
            break


        frame, result = analyzer.analyze(frame)


        if result["face_detected"]:

            cv2.putText(
                frame,
                "Face Detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Attention: {result['attention_score']}%",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Head: {result['head_pose']}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Confidence: {result['confidence_score']}%",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

        cv2.imshow(
            "InterviewLens Camera",
            frame
        )


        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_camera()
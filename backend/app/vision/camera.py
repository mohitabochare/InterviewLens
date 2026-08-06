import cv2
from app.vision.analyzer import FaceAnalyzer


def start_camera():
    cap = cv2.VideoCapture(0)
    analyzer = FaceAnalyzer()

    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame.")
            break

        frame, detected = analyzer.analyze(frame)

        if detected:
            cv2.putText(
                frame,
                "Face Detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
        else:
            cv2.putText(
                frame,
                "No Face",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )

        cv2.imshow("InterviewLens Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_camera()
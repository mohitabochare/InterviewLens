import requests
import cv2

from app.vision.analyzer import FaceAnalyzer
from app.voice.record_audio import record_test_clip
from app.voice.analyzer import VoiceAnalyzer
from app.answer_intelligence.evaluator import evaluate_answer, PRACTICE_QUESTION

API_BASE = "http://127.0.0.1:8000"
AUDIO_PATH = "app/voice/test_recording.wav"


def start_api_session():
    try:
        response = requests.post(f"{API_BASE}/session/start", timeout=5)
        response.raise_for_status()
        return response.json()["session_id"]
    except requests.exceptions.ConnectionError:
        print("Error: Could not reach the backend server.")
        print("Make sure it's running: uvicorn app.main:app --reload")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error starting session: {e}")
        return None


def end_api_session(session_id, metrics: dict):
    try:
        response = requests.post(
            f"{API_BASE}/session/{session_id}/end",
            json=metrics,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error ending session (data may be lost): {e}")
        return None


def run_vision_capture():
    try:
        analyzer = FaceAnalyzer()
    except Exception as e:
        print(f"Error loading vision models: {e}")
        return None, None

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access camera.")
        return None, None

    attention_scores = []
    confidence_scores = []

    print("Recording video... press 'q' to end the interview.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Warning: Failed to read a frame, stopping.")
                break

            frame, result = analyzer.analyze(frame)

            if result["face_detected"]:
                attention_scores.append(result["attention_score"])
                confidence_scores.append(result["confidence_score"])

                cv2.putText(
                    frame, f"Confidence: {result['confidence_score']}%",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
                )

            cv2.imshow("InterviewLens - Live Session", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    avg_attention = (
        sum(attention_scores) / len(attention_scores)
        if attention_scores else 0
    )
    avg_confidence = (
        sum(confidence_scores) / len(confidence_scores)
        if confidence_scores else 0
    )

    return round(avg_attention, 1), round(avg_confidence, 1)


def run_voice_capture():
    try:
        print("Recording audio response...")
        record_test_clip()

        voice_analyzer = VoiceAnalyzer()
        result = voice_analyzer.analyze(AUDIO_PATH)
        return result
    except Exception as e:
        print(f"Error during voice analysis: {e}")
        return None


def run_live_session():
    session_id = start_api_session()
    if session_id is None:
        print("Aborting: no session was created.")
        return

    print(f"Session {session_id} started.")

    eye_contact_score, confidence_score = run_vision_capture()

    print(f"\nInterview question: {PRACTICE_QUESTION}")
    voice_result = run_voice_capture()

    metrics = {
        "eye_contact_score": eye_contact_score,
        "confidence_score": confidence_score,
    }

    if voice_result:
        metrics["speaking_rate_wpm"] = voice_result["speaking_rate_wpm"]
        metrics["filler_word_count"] = voice_result["filler_word_count"]
        metrics["pause_count"] = voice_result["pause_count"]
        metrics["transcript"] = voice_result["transcript"]

        print("Evaluating answer...")
        evaluation = evaluate_answer(PRACTICE_QUESTION, voice_result["transcript"])
        metrics["star_present"] = evaluation.get("star_present")
        metrics["answer_strengths"] = evaluation.get("strengths")
        metrics["answer_improvements"] = evaluation.get("improvements")

    result = end_api_session(session_id, metrics)

    if result:
        print("\nSession ended. Final report:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print(f"Session {session_id} may not have been saved properly.")


if __name__ == "__main__":
    run_live_session()
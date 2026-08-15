from faster_whisper import WhisperModel

AUDIO_PATH = "app/voice/test_recording.wav"


def transcribe_test_clip():
    print("Loading speech-to-text model (first run downloads it, may take a moment)...")
    model = WhisperModel("base", device="cpu", compute_type="int8")

    print("Transcribing...")
    segments, info = model.transcribe(AUDIO_PATH)

    print(f"Detected language: {info.language} (confidence: {info.language_probability:.2f})")
    print("\nTranscript:")

    full_text = ""
    for segment in segments:
        print(f"  [{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        full_text += segment.text

    print(f"\nFull text: {full_text.strip()}")


if __name__ == "__main__":
    transcribe_test_clip()
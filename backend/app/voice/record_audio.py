import sounddevice as sd
from scipy.io.wavfile import write

SAMPLE_RATE = 16000
DURATION_SECONDS = 5
OUTPUT_PATH = "app/voice/test_recording.wav"


def record_test_clip():
    print(f"Recording for {DURATION_SECONDS} seconds... speak now.")

    audio = sd.rec(
        int(DURATION_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
    )
    sd.wait()

    write(OUTPUT_PATH, SAMPLE_RATE, audio)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    record_test_clip()
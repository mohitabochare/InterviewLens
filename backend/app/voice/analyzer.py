from faster_whisper import WhisperModel
from scipy.io import wavfile
import numpy as np
import re


FILLER_WORDS = ["um", "uh", "like", "actually", "basically", "literally", "you know"]


class VoiceAnalyzer:
    def __init__(self):
        self.model = WhisperModel("base", device="cpu", compute_type="int8")

    def analyze(self, audio_path: str) -> dict:
        segments, info = self.model.transcribe(audio_path)

        full_text = ""
        segment_list = []
        for segment in segments:
            full_text += segment.text
            segment_list.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
            })

        full_text = full_text.strip()
        duration_minutes = segment_list[-1]["end"] / 60 if segment_list else 0
        word_count = len(full_text.split())

        speaking_rate = (
            round(word_count / duration_minutes)
            if duration_minutes > 0 else 0
        )

        filler_count, filler_breakdown = self._count_filler_words(full_text)
        pause_count = self.detect_pauses(audio_path)

        return {
            "transcript": full_text,
            "word_count": word_count,
            "duration_minutes": round(duration_minutes, 2),
            "speaking_rate_wpm": speaking_rate,
            "language": info.language,
            "filler_word_count": filler_count,
            "filler_word_breakdown": filler_breakdown,
            "pause_count": pause_count,
        }

    def _count_filler_words(self, text: str):
        text_lower = text.lower()
        breakdown = {}

        for filler in FILLER_WORDS:
            pattern = r"\b" + re.escape(filler) + r"\b"
            matches = re.findall(pattern, text_lower)
            if matches:
                breakdown[filler] = len(matches)

        total = sum(breakdown.values())
        return total, breakdown

    def detect_pauses(self, audio_path: str, silence_threshold=500, min_pause_duration=0.5):
        rate, data = wavfile.read(audio_path)

        window_size = int(rate * 0.05)
        pause_count = 0
        in_pause = False
        pause_start = 0

        for i in range(0, len(data) - window_size, window_size):
            window = data[i:i + window_size]
            volume = np.abs(window).mean()

            if volume < silence_threshold:
                if not in_pause:
                    in_pause = True
                    pause_start = i / rate
            else:
                if in_pause:
                    pause_duration = (i / rate) - pause_start
                    if pause_duration >= min_pause_duration:
                        pause_count += 1
                    in_pause = False

        return pause_count


if __name__ == "__main__":
    analyzer = VoiceAnalyzer()
    result = analyzer.analyze("app/voice/test_recording.wav")

    print(f"Transcript: {result['transcript']}")
    print(f"Word count: {result['word_count']}")
    print(f"Duration: {result['duration_minutes']} min")
    print(f"Speaking rate: {result['speaking_rate_wpm']} words/min")
    print(f"Filler words: {result['filler_word_count']}")
    print(f"Breakdown: {result['filler_word_breakdown']}")
    print(f"Long pauses: {result['pause_count']}")
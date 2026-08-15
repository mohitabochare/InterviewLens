# InterviewLens

An AI-powered mock interview analysis platform. Records a candidate's video and voice during a practice interview, analyzes their behavior in real time, and produces a scored report.

> **Status:** core pipeline working end-to-end — vision analysis, voice analysis, and session persistence are all built and integrated. See [PROJECT_CONTEXT.md](./PROJECT_CONTEXT.md) for known limitations and what's intentionally deferred.

## What it does

Run one command, sit through a short practice interview, and get back a real report:

- **Vision analysis** — face detection, eye contact tracking, head pose, and a confidence score from a model trained on labeled interview footage
- **Voice analysis** — speech-to-text transcription, speaking rate (words/min), filler word detection, and pause detection
- **Session storage** — every interview is saved to a database and retrievable later via a REST API

## Tech stack

| Layer | Choice |
|---|---|
| Backend | Python 3.13, FastAPI |
| Database | SQLite via SQLAlchemy |
| Computer vision | OpenCV, MediaPipe (BlazeFace, Face Landmarker) |
| Confidence scoring | scikit-learn logistic regression, trained on self-collected labeled data |
| Speech-to-text | faster-whisper (local, no API key required) |
| Testing | Pytest |

## Project structure
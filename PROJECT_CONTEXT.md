## Current state (as of this session)

Built and verified working, end to end:
- Vision pipeline: face detection, eye tracking (gaze measured relative to
  eye socket, not frame — decoupled from head position), head pose, and a
  logistic regression confidence model trained on self-collected labeled data
- Voice pipeline: audio capture, speech-to-text (faster-whisper), speaking
  rate, filler word detection, silence-based pause detection
- Backend: full session lifecycle (start/end/get/list), persisted to SQLite
- Integration: one script (`live_session.py`) runs a full interview —
  camera capture, then audio capture — and submits a combined report
- Answer intelligence: transcripts are evaluated against the STAR format
  (Situation, Task, Action, Result) via the Gemini API, returning structured
  strengths/improvements — genuinely wired into the live session flow, not
  a standalone demo.
## Known limitations

- The trained confidence model was fit on a small, self-collected dataset
  (~150 labeled frames, one person, one room/lighting setup). It is not
  claimed to generalize to other people, cameras, or environments.
- Head pose detection uses landmark-ratio thresholds, not full 3D pose
  estimation (yaw/pitch/roll). It can misclassify extreme angles.
- Vision and voice capture currently run 
- The interview question is currently a single hardcoded practice question
  ("Tell me about a project you've worked on"), not dynamically generated
  or selectable. Real interview variety is future work.
- Answer evaluation depends on an external API (Gemini) and a network
  connection — unlike vision and voice, which run entirely locally. If the
  API is unavailable or the key is invalid, evaluation fails gracefully
  (returns empty feedback) but the feature itself won't work offline.
- The AI evaluator's judgment (what counts as "good" STAR structure) comes
  from an off-the-shelf LLM's general reasoning, not from any interview-
  specific training or validation against real hiring outcomes.
**sequentially**, not
  simultaneously — the camera loop finishes first, then a separate fixed
  audio recording happens. A real interview would want both running at once;
  this was a deliberate scope cut given time constraints.
- The filler word list and the pause-detection silence threshold are
  reasonable manual choices, not tuned against real interview data.
- No AI-based answer evaluation yet (judging the *content* of what someone
  said) — only behavioral signals (how they said it).
- No frontend — the API and `/docs` (Swagger UI) are the only interfaces.
- No authentication — sessions aren't tied to individual users.
- SQLite is used for simplicity, not intended for concurrent/production use.
# TODO

A running checklist. Keep it honest — check things off as you go, don't
pre-fill things you haven't actually done.

## Phase 0 — Scaffold (current)
- [x] Create repo structure
- [x] Backend skeleton (FastAPI) with a health-check route
- [x] Core docs (README, PROJECT_CONTEXT, CHANGELOG, TODO)
- [ ] Push to GitHub, confirm `.gitignore` is actually ignoring what it should
- [ ] Set up a virtual environment and confirm `uvicorn app.main:app --reload` runs

## Phase 1 — Backend foundations
- [ ] Add `.env` handling and confirm `core/config.py` loads settings correctly
- [ ] Add a proper logging setup
- [ ] Decide on a database (SQLite for dev is fine to start)
- [ ] Add first real data model (e.g. `InterviewSession`)
- [ ] Add first real CRUD endpoint (e.g. create/list interview sessions)
- [ ] Add basic request/response validation via Pydantic schemas
- [ ] Write tests for the above (pytest)

## Phase 2 — Auth & users
- [ ] Decide on auth approach (e.g. simple email/password + JWT, or OAuth)
- [ ] User model + registration/login endpoints
- [ ] Protect routes that should require login

## Phase 3 — Frontend
- [ ] Choose frontend framework (React/Next.js recommended, but your call)
- [ ] Scaffold frontend project inside `frontend/`
- [ ] Connect frontend to backend health-check endpoint as a smoke test
- [ ] Build basic pages: landing, dashboard, session detail

## Phase 4 — Interview session flow (still no AI)
- [ ] Define what an "interview session" actually contains (questions, timing, metadata)
- [ ] Build the non-AI mock interview flow: user answers text-based practice questions
- [ ] Store and display past sessions

## Phase 5 — AI features (explicitly deferred — do not start early)
- [ ] Question generation
- [ ] Answer evaluation / feedback
- [ ] Speech-to-text integration
- [ ] Computer vision (posture/eye-contact feedback, etc.)

## Ongoing / housekeeping
- [ ] Keep CHANGELOG.md updated with every meaningful change
- [ ] Keep PROJECT_CONTEXT.md updated if scope or architecture decisions change
- [ ] Add screenshots to README once there's a UI worth showing

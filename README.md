# InterviewLens

A mock interview platform, built as a clean, modular portfolio project.

> **Status:** early scaffold. Core AI/ML/CV/speech features are intentionally
> not yet implemented — see [PROJECT_CONTEXT.md](./PROJECT_CONTEXT.md) for why.

## What is this?

InterviewLens aims to let users practice for job interviews through
structured mock sessions, with feedback features planned for a later phase.
Right now, the focus is on building a solid, well-organized foundation:
a typed REST API, a clear data model, and a maintainable project structure.

## Tech stack

| Layer | Choice |
|---|---|
| Backend | Python 3.11+, FastAPI |
| Backend testing | Pytest |
| Frontend | TBD (see `frontend/README.md`) |
| Database | SQLite (dev), swappable later |

## Project structure

```
InterviewLens/
├── backend/
│   └── app/
│       ├── main.py          # FastAPI app entrypoint
│       ├── core/             # config, settings
│       ├── api/routes/       # route handlers (thin)
│       ├── services/         # business logic
│       ├── models/           # DB models
│       └── schemas/          # Pydantic request/response schemas
├── frontend/                 # placeholder — framework TBD
├── PROJECT_CONTEXT.md        # scope, architecture decisions, non-goals
├── TODO.md                   # phased development checklist
└── CHANGELOG.md
```

## Getting started (backend)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then visit:
- API root: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Running tests

```bash
cd backend
pytest
```

## Roadmap

See [TODO.md](./TODO.md) for the full phased plan. In short:

1. ✅ Project scaffold
2. Backend foundations (DB, real endpoints, tests)
3. Auth
4. Frontend
5. Non-AI interview session flow
6. AI features (question generation, feedback, speech/CV) — deferred

## Contributing / scope notes

This is a personal portfolio project. If you're an AI assistant or a future
contributor picking this up, read [PROJECT_CONTEXT.md](./PROJECT_CONTEXT.md)
first — it defines what's explicitly in and out of scope.

## License

MIT — see [LICENSE](./LICENSE).

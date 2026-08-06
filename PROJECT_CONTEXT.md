# Project Context

This file exists so that anyone (including a future you, or an AI assistant
helping you) can understand the intent, scope, and boundaries of this project
without re-deriving them from scratch. Update this file whenever a scope or
architecture decision changes.

## What this project is

**InterviewLens** is a mock interview platform, built as a portfolio project
to demonstrate clean, modular, production-style engineering practices — not
to demonstrate AI/ML sophistication (yet).

Target audience for the *code itself*: a recruiter or engineer skimming the
repo should immediately understand the structure and see deliberate,
readable decisions rather than framework sprawl.

## Current scope (what exists or is actively being built)

- A FastAPI backend with a clean, layered structure (`api → services → models`)
- Basic REST endpoints for managing interview sessions
- A frontend (framework TBD) that talks to the backend
- Standard project hygiene: tests, docs, changelog, licensing

## Explicitly out of scope for now

Do not implement, scaffold, or add dependencies for any of the following
until the project explicitly reaches "Phase 5" in `TODO.md`:

- AI/ML question generation or answer evaluation
- Computer vision (facial expression, eye contact, posture analysis)
- Speech-to-text or audio processing
- Any third-party AI API integration (OpenAI, Anthropic, etc.)

This is a deliberate constraint, not an oversight. The goal right now is a
solid, non-AI foundation: data models, API design, auth, and a working UI
skeleton. AI features will be added later as isolated, swappable services —
not bolted into the core request/response flow.

## Architecture decisions and why

| Decision | Reasoning |
|---|---|
| **FastAPI** over Flask/Django | Async-native, automatic OpenAPI docs, strong typing via Pydantic, minimal boilerplate — good fit for a solo portfolio project and for AI integrations later. |
| **Layered backend (api / services / models / schemas)** | Keeps route handlers thin. Business logic lives in `services/`, so it's testable without spinning up HTTP. No repository pattern or DI framework — that's over-engineering for this project's size. |
| **SQLite for early development** (planned) | Zero setup cost. Swappable for Postgres later since we're not hand-rolling raw SQL. |
| **Frontend kept separate, framework undecided** | Backend and frontend should be independently deployable. Framework choice is deferred until Phase 3 so it isn't picked under scaffolding pressure. |
| **No AI dependencies in `requirements.txt` yet** | Matches the explicit "not yet" scope above. Adding them early would create dead weight and misleading signals about project maturity. |

## Non-goals

- This is not trying to be a scalable, multi-tenant SaaS from day one.
- No microservices. One backend service, one frontend, until there's a
  concrete reason to split further.
- No premature optimization — correctness and readability first.

## How to use this file

If you (or an AI assistant) are about to make an architectural decision —
adding a new dependency, restructuring folders, introducing a new pattern —
check here first. If it contradicts something above, either don't do it, or
update this file to reflect the new decision *and* explain why.

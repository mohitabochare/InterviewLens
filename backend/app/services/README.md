# services/

Business logic lives here, kept separate from route handlers (`api/routes/`)
and data models (`models/`). Routes should stay thin: parse request, call a
service function, return response.

Nothing here yet — first service will likely be session management logic
(Phase 1 in TODO.md).

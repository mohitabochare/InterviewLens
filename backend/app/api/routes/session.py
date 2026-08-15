import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import session_service
from app.schemas.session import (
    SessionStartResponse,
    SessionEndRequest,
    SessionResponse,
)

router = APIRouter(prefix="/session", tags=["session"])


def _to_response(session) -> SessionResponse:
    return SessionResponse(
        session_id=session.id,
        start_time=session.start_time,
        end_time=session.end_time,
        duration_seconds=session.duration_seconds,
        eye_contact_score=session.eye_contact_score,
        confidence_score=session.confidence_score,
        speaking_rate_wpm=session.speaking_rate_wpm,
        filler_word_count=session.filler_word_count,
        pause_count=session.pause_count,
        transcript=session.transcript,
        star_present=session.star_present,
        answer_strengths=json.loads(session.answer_strengths) if session.answer_strengths else None,
        answer_improvements=json.loads(session.answer_improvements) if session.answer_improvements else None,
    )


@router.post("/start", response_model=SessionStartResponse)
def start_session(db: Session = Depends(get_db)):
    session = session_service.create_session(db)
    return SessionStartResponse(
        session_id=session.id,
        start_time=session.start_time,
    )


@router.post("/{session_id}/end", response_model=SessionResponse)
def end_session(
    session_id: int,
    payload: SessionEndRequest,
    db: Session = Depends(get_db),
):
    session = session_service.end_session(
        db,
        session_id,
        eye_contact_score=payload.eye_contact_score,
        confidence_score=payload.confidence_score,
        speaking_rate_wpm=payload.speaking_rate_wpm,
        filler_word_count=payload.filler_word_count,
        pause_count=payload.pause_count,
        transcript=payload.transcript,
        star_present=payload.star_present,
        answer_strengths=payload.answer_strengths,
        answer_improvements=payload.answer_improvements,
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return _to_response(session)


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = session_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return _to_response(session)


@router.get("/", response_model=List[SessionResponse])
def list_sessions(db: Session = Depends(get_db)):
    sessions = session_service.get_all_sessions(db)
    return [_to_response(s) for s in sessions]
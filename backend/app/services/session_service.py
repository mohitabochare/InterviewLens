from datetime import datetime
import json

from sqlalchemy.orm import Session

from app.models.session import InterviewSession


def create_session(db: Session) -> InterviewSession:
    session = InterviewSession(start_time=datetime.utcnow())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def end_session(
    db: Session,
    session_id: int,
    eye_contact_score: float = None,
    confidence_score: float = None,
    speaking_rate_wpm: float = None,
    filler_word_count: int = None,
    pause_count: int = None,
    transcript: str = None,
    star_present: bool = None,
    answer_strengths: list = None,
    answer_improvements: list = None,
) -> InterviewSession | None:

    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id
    ).first()

    if not session:
        return None

    session.end_time = datetime.utcnow()
    session.duration_seconds = (
        session.end_time - session.start_time
    ).total_seconds()

    if eye_contact_score is not None:
        session.eye_contact_score = eye_contact_score
    if confidence_score is not None:
        session.confidence_score = confidence_score
    if speaking_rate_wpm is not None:
        session.speaking_rate_wpm = speaking_rate_wpm
    if filler_word_count is not None:
        session.filler_word_count = filler_word_count
    if pause_count is not None:
        session.pause_count = pause_count
    if transcript is not None:
        session.transcript = transcript
    if star_present is not None:
        session.star_present = star_present
    if answer_strengths is not None:
        session.answer_strengths = json.dumps(answer_strengths)
    if answer_improvements is not None:
        session.answer_improvements = json.dumps(answer_improvements)

    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: int) -> InterviewSession | None:
    return db.query(InterviewSession).filter(
        InterviewSession.id == session_id
    ).first()


def get_all_sessions(db: Session):
    return db.query(InterviewSession).order_by(
        InterviewSession.start_time.desc()
    ).all()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.services import session_service


def get_test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSessionLocal = sessionmaker(bind=engine)
    return TestSessionLocal()


def test_create_and_get_session():
    db = get_test_db()

    session = session_service.create_session(db)
    assert session.id is not None
    assert session.end_time is None

    fetched = session_service.get_session(db, session.id)
    assert fetched.id == session.id


def test_end_session_sets_duration():
    db = get_test_db()

    session = session_service.create_session(db)
    ended = session_service.end_session(
        db, session.id, eye_contact_score=85.0, confidence_score=90.0
    )

    assert ended.end_time is not None
    assert ended.duration_seconds >= 0
    assert ended.eye_contact_score == 85.0
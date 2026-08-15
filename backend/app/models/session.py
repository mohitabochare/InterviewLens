from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Float, String, Boolean
from app.core.database import Base


class InterviewSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)

    eye_contact_score = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)

    speaking_rate_wpm = Column(Float, nullable=True)
    filler_word_count = Column(Integer, nullable=True)
    pause_count = Column(Integer, nullable=True)
    transcript = Column(String, nullable=True)

    star_present = Column(Boolean, nullable=True)
    answer_strengths = Column(String, nullable=True)
    answer_improvements = Column(String, nullable=True)
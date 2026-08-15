from datetime import datetime
from pydantic import BaseModel


class SessionStartResponse(BaseModel):
    session_id: int
    start_time: datetime

    class Config:
        from_attributes = True


class SessionEndRequest(BaseModel):
    eye_contact_score: float | None = None
    confidence_score: float | None = None
    speaking_rate_wpm: float | None = None
    filler_word_count: int | None = None
    pause_count: int | None = None
    transcript: str | None = None
    star_present: bool | None = None
    answer_strengths: list[str] | None = None
    answer_improvements: list[str] | None = None


    


class SessionResponse(BaseModel):
    session_id: int
    start_time: datetime
    end_time: datetime | None
    duration_seconds: float | None
    eye_contact_score: float | None
    confidence_score: float | None
    speaking_rate_wpm: float | None
    filler_word_count: int | None
    pause_count: int | None
    transcript: str | None

    star_present: bool | None = None
    answer_strengths: list[str] | None = None
    answer_improvements: list[str] | None = None

   
    class Config:
        from_attributes = True

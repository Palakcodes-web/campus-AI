from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date, time


class AnnouncementCreate(BaseModel):
    raw_text: str
    source: Optional[str] = None
    sender: Optional[str] = None
    category: Optional[str] = None
    timestamp: Optional[datetime] = None


class AnnouncementBatchCreate(BaseModel):
    announcements: List[AnnouncementCreate]


class AnnouncementOut(BaseModel):
    id: int
    raw_text: str
    source: Optional[str] = None
    sender: Optional[str] = None
    category: Optional[str] = None
    submitted_at: datetime

    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    organizer: Optional[str] = None

    event_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    registration_deadline: Optional[datetime] = None

    seat_limit: Optional[int] = None
    registration_required: Optional[bool] = None
    mandatory: Optional[bool] = None

    status: str
    duplicate_of_id: Optional[int] = None

    priority_score: Optional[int] = None
    priority_label: Optional[str] = None
    why_text: Optional[str] = None
    missing_info: Optional[List[str]] = []

    confidence_score: Optional[float] = None
    extraction_method: Optional[str] = None
    processed: bool

    class Config:
        from_attributes = True


class ProcessResponse(BaseModel):
    processed_count: int
    announcements: List[AnnouncementOut]
from pydantic import BaseModel
from typing import Optional
from datetime import time, datetime


class TimetableEntryOut(BaseModel):
    id: int
    branch: str
    year: int
    section: Optional[str] = None
    day_of_week: str
    start_time: time
    end_time: time
    subject_code: Optional[str] = None
    subject_name: str
    faculty: Optional[str] = None
    venue: Optional[str] = None
    is_lab: Optional[bool] = None

    class Config:
        from_attributes = True


class TimetableConflictOut(BaseModel):
    id: int
    student_id: int
    event_id: int
    timetable_entry_id: int
    event_title: Optional[str] = None
    class_title: Optional[str] = None
    venue: Optional[str] = None
    overlap_start: Optional[datetime] = None
    overlap_end: Optional[datetime] = None
    explanation: str
    suggested_consideration: Optional[str] = None

    class Config:
        from_attributes = True
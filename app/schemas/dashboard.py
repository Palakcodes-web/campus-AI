from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ConflictOut(BaseModel):
    id: int
    student_id: int
    event_a_id: int
    event_b_id: int
    event_a_title: Optional[str] = None
    event_b_title: Optional[str] = None
    overlap_start: Optional[datetime] = None
    overlap_end: Optional[datetime] = None
    explanation: str
    suggested_consideration: Optional[str] = None

    class Config:
        from_attributes = True


class ActionOut(BaseModel):
    id: int
    announcement_id: int
    action_text: str
    why_text: Optional[str] = None
    deadline: Optional[datetime] = None
    urgency: Optional[str] = None
    missing_info: Optional[List[str]] = []

    class Config:
        from_attributes = True


class DashboardOut(BaseModel):
    student_id: int
    top_priorities: List[dict]
    conflicts: List[ConflictOut]
    action_plan: List[ActionOut]
    
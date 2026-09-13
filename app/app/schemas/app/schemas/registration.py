from pydantic import BaseModel
from datetime import datetime


class RegistrationCreate(BaseModel):
    announcement_id: int


class RegistrationOut(BaseModel):
    id: int
    student_id: int
    announcement_id: int
    registered_at: datetime

    class Config:
        from_attributes = True
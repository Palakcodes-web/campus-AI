from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class StudentCreate(BaseModel):
    name: str
    department: Optional[str] = None
    year: Optional[int] = None
    semester: Optional[int] = None
    section: Optional[str] = None
    interests: Optional[List[str]] = []


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    year: Optional[int] = None
    semester: Optional[int] = None
    section: Optional[str] = None
    interests: Optional[List[str]] = None


class StudentOut(BaseModel):
    id: int
    name: str
    department: Optional[str] = None
    year: Optional[int] = None
    semester: Optional[int] = None
    section: Optional[str] = None
    interests: Optional[List[str]] = []
    created_at: datetime

    class Config:
        from_attributes = True
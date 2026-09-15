from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

from app.database import get_db
from app.models.student import Student
from app.services.ask_service import ask_campus_ai

router = APIRouter(prefix="/api", tags=["ask"])


class AskRequest(BaseModel):
    question: str
    student_id: Optional[int] = Field(default=None, examples=[None])


@router.post("/ask")
def ask_campus_ai_route(payload: AskRequest, db: Session = Depends(get_db)):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="question must not be empty")

    if payload.student_id is not None:
        student = db.query(Student).filter(Student.id == payload.student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

    return ask_campus_ai(db, payload.question, payload.student_id)
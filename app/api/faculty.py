from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.faculty_service import list_faculty, get_faculty_detail

router = APIRouter(prefix="/api", tags=["faculty"])


@router.get("/faculty")
def get_faculty(
    name: Optional[str] = None,
    branch: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if name:
        detail = get_faculty_detail(db, name)
        if not detail:
            raise HTTPException(status_code=404, detail="Faculty not found")
        return detail

    return {"faculty": list_faculty(db, branch)}
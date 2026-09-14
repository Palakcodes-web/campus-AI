from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.timetable_services import get_timetable_by_branch_year

router = APIRouter(prefix="/api", tags=["timetable"])


@router.get("/timetable")
def get_timetable(
    branch: str = Query(...),
    year: int = Query(...),
    section: Optional[str] = None,
    db: Session = Depends(get_db),
):
    entries = get_timetable_by_branch_year(db, branch, year, section)

    return {
        "branch": branch,
        "year": year,
        "section": section,
        "entries": [
            {
                "id": e.id,
                "day_of_week": e.day_of_week.value,
                "start_time": e.start_time,
                "end_time": e.end_time,
                "subject_code": e.subject_code,
                "subject_name": e.subject_name,
                "faculty": e.faculty,
                "venue": e.venue,
                "is_lab": e.is_lab,
            }
            for e in entries
        ],
    }
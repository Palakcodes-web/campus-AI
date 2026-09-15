from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.faculty_service import (
    list_faculty, get_faculty_detail,
    search_faculty, get_faculty_timetable, get_faculty_availability,
)

router = APIRouter(prefix="/api", tags=["faculty"])


@router.get("/faculty", summary="Search faculty (partial, case-insensitive) or list by branch")
def get_faculty(
    name: Optional[str] = None,
    branch: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if name:
        matches = search_faculty(db, name)
        return {
            "faculty": [
                {"name": f.name, "department": f.department, "subjects": sorted({
                    s.timetable_entry.subject_name for s in f.schedules
                })}
                for f in matches
            ]
        }

    return {"faculty": list_faculty(db, branch)}


@router.get("/faculty/{faculty_name}/timetable", summary="Faculty weekly timetable, sorted Mon-Sat by start time")
def faculty_timetable(faculty_name: str, db: Session = Depends(get_db)):
    result = get_faculty_timetable(db, faculty_name)
    if not result:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return result


@router.get("/faculty/{faculty_name}/availability", summary="Free/busy slots per the uploaded timetable ONLY")
def faculty_availability(faculty_name: str, db: Session = Depends(get_db)):
    result = get_faculty_availability(db, faculty_name)
    if not result:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return result
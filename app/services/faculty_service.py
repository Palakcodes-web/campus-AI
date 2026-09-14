from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.timetable import TimetableEntry


def list_faculty(db: Session, branch: Optional[str] = None) -> List[dict]:
    """Aggregated purely from TimetableEntry rows — no separate Faculty
    table exists, so nothing here is invented beyond what the seeded
    timetable data actually contains."""
    query = db.query(TimetableEntry).filter(TimetableEntry.faculty.isnot(None))
    if branch:
        query = query.filter(TimetableEntry.branch == branch)
    entries = query.all()

    faculty_map = {}
    for e in entries:
        bucket = faculty_map.setdefault(e.faculty, {"subjects": set(), "venues": set(), "branches": set()})
        bucket["subjects"].add(e.subject_name)
        if e.venue:
            bucket["venues"].add(e.venue)
        bucket["branches"].add(e.branch)

    return [
        {
            "name": name,
            "subjects": sorted(data["subjects"]),
            "venues": sorted(data["venues"]),
            "branches": sorted(data["branches"]),
        }
        for name, data in faculty_map.items()
    ]


def get_faculty_detail(db: Session, name: str) -> Optional[dict]:
    entries = db.query(TimetableEntry).filter(TimetableEntry.faculty == name).all()
    if not entries:
        return None

    schedule = [
        {
            "day_of_week": e.day_of_week.value,
            "start_time": e.start_time,
            "end_time": e.end_time,
            "subject_name": e.subject_name,
            "venue": e.venue,
            "branch": e.branch,
            "year": e.year,
        }
        for e in entries
    ]
    return {
        "name": name,
        "subjects": sorted({e.subject_name for e in entries}),
        "schedule": schedule,
    }
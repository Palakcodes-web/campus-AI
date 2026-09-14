from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.timetable import TimetableEntry, TimetableConflict, Weekday
from app.models.event import Event
from app.models.registration import StudentRegistration
from app.models.announcement import Announcement
from app.models.student import Student

WEEKDAY_INDEX = {
    0: Weekday.MONDAY, 1: Weekday.TUESDAY, 2: Weekday.WEDNESDAY,
    3: Weekday.THURSDAY, 4: Weekday.FRIDAY, 5: Weekday.SATURDAY,
}


def get_timetable_for_student(db: Session, student: Student) -> List[TimetableEntry]:
    """Matches by department (used as branch) + year. Section filters only
    apply when both the student and the entry specify one — entries with
    no section are treated as applying to the whole class."""
    if not student.department or not student.year:
        return []

    entries = db.query(TimetableEntry).filter(
        TimetableEntry.branch == student.department,
        TimetableEntry.year == student.year,
    ).all()

    if getattr(student, "section", None):
        entries = [e for e in entries if e.section is None or e.section == student.section]

    return entries


def _get_registered_events_with_time(db: Session, student_id: int) -> List[Event]:
    reg_ann_ids = [
        r.announcement_id
        for r in db.query(StudentRegistration).filter(StudentRegistration.student_id == student_id).all()
    ]
    if not reg_ann_ids:
        return []
    events = db.query(Event).filter(Event.announcement_id.in_(reg_ann_ids)).all()
    return [e for e in events if e.event_date and e.start_time]

def detect_timetable_conflicts_for_student(db: Session, student: Student) -> List[TimetableConflict]:
    """Checks a student's registered one-off events against their fixed
    weekly class schedule. States the clash only — never tells the
    student whether to skip class or the event."""
    db.query(TimetableConflict).filter(TimetableConflict.student_id == student.id).delete()

    timetable_entries = get_timetable_for_student(db, student)
    if not timetable_entries:
        db.commit()
        return []

    events = _get_registered_events_with_time(db, student.id)
    detected: List[TimetableConflict] = []

    for event in events:
        weekday = WEEKDAY_INDEX.get(event.event_date.weekday())
        if weekday is None:
            continue
        same_day_entries = [t for t in timetable_entries if t.day_of_week == weekday]

        event_start = datetime.combine(event.event_date, event.start_time)
        event_end = datetime.combine(event.event_date, event.end_time) if event.end_time else event_start

        for entry in same_day_entries:
            entry_start = datetime.combine(event.event_date, entry.start_time)
            entry_end = datetime.combine(event.event_date, entry.end_time)

            overlap_start = max(event_start, entry_start)
            overlap_end = min(event_end, entry_end)

            if overlap_start < overlap_end:
                conflict = TimetableConflict(
                    student_id=student.id,
                    event_id=event.id,
                    timetable_entry_id=entry.id,
                    overlap_start=overlap_start,
                    overlap_end=overlap_end,
                )
                db.add(conflict)
                detected.append(conflict)

    db.commit()
    for c in detected:
        db.refresh(c)
    return detected


def build_timetable_conflict_explanation(db: Session, conflict: TimetableConflict) -> dict:
    event = db.query(Event).filter(Event.id == conflict.event_id).first()
    entry = db.query(TimetableEntry).filter(TimetableEntry.id == conflict.timetable_entry_id).first()
    ann = db.query(Announcement).filter(Announcement.id == event.announcement_id).first() if event else None

    event_title = (ann.title if ann else None) or "Registered event"
    class_title = entry.subject_name if entry else "a scheduled class"

    start_str = conflict.overlap_start.strftime("%I:%M %p") if conflict.overlap_start else "unknown"
    end_str = conflict.overlap_end.strftime("%I:%M %p") if conflict.overlap_end else "unknown"

    explanation = f"'{event_title}' overlaps with your regular '{class_title}' class between {start_str} and {end_str}."
    suggestion = "Class attendance is mandatory by default — check with faculty if you need to miss it for the registered event."

    return {
        "id": conflict.id,
        "student_id": conflict.student_id,
        "event_id": conflict.event_id,
        "timetable_entry_id": conflict.timetable_entry_id,
        "event_title": event_title,
        "class_title": class_title,
        "venue": entry.venue if entry else None,
        "overlap_start": conflict.overlap_start,
        "overlap_end": conflict.overlap_end,
        "explanation": explanation,
        "suggested_consideration": suggestion,
    }

def get_timetable_by_branch_year(db: Session, branch: str, year: int, section: str = None) -> List[TimetableEntry]:
    """Direct lookup for the /api/timetable endpoint — doesn't require a
    Student object. Branch matching is case-insensitive (e.g. "cse" and
    "CSE" both match) so the frontend doesn't need exact seeded casing.
    Entries with no section apply to the whole class; entries with a
    section only match when it equals the one requested."""
    entries = db.query(TimetableEntry).filter(
        func.lower(TimetableEntry.branch) == branch.strip().lower(),
        TimetableEntry.year == year,
    ).all()

    if section:
        entries = [e for e in entries if e.section is None or e.section == section]

    return entries
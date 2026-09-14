from datetime import datetime, date, time
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.registration import StudentRegistration
from app.models.announcement import Announcement
from app.models.conflict import Conflict


def _combine(d: date, t: time) -> datetime:
    return datetime.combine(d, t)


def get_student_committed_events(db: Session, student_id: int) -> List[Event]:
    """A student's 'committed' events = ones they've registered for. Only
    these are checked against each other for conflicts — we don't warn
    about clashes between events the student never signed up for."""
    reg_ann_ids = [
        r.announcement_id
        for r in db.query(StudentRegistration).filter(StudentRegistration.student_id == student_id).all()
    ]
    if not reg_ann_ids:
        return []
    return db.query(Event).filter(Event.announcement_id.in_(reg_ann_ids)).all()


def detect_conflicts_for_student(db: Session, student_id: int) -> List[Conflict]:
    events = get_student_committed_events(db, student_id)
    detected: List[Conflict] = []

    # clear stale conflicts for this student before recomputing
    db.query(Conflict).filter(Conflict.student_id == student_id).delete()

    usable = [e for e in events if e.event_date and e.start_time]
    for i in range(len(usable)):
        for j in range(i + 1, len(usable)):
            a, b = usable[i], usable[j]
            if a.event_date != b.event_date:
                continue

            a_start = _combine(a.event_date, a.start_time)
            a_end = _combine(a.event_date, a.end_time) if a.end_time else a_start
            b_start = _combine(b.event_date, b.start_time)
            b_end = _combine(b.event_date, b.end_time) if b.end_time else b_start

            overlap_start = max(a_start, b_start)
            overlap_end = min(a_end, b_end)

            if overlap_start < overlap_end:
                conflict = Conflict(
                    student_id=student_id,
                    event_a_id=a.id,
                    event_b_id=b.id,
                    overlap_start=overlap_start,
                    overlap_end=overlap_end,
                )
                db.add(conflict)
                detected.append(conflict)

    db.commit()
    for c in detected:
        db.refresh(c)
    return detected


def build_conflict_explanation(db: Session, conflict: Conflict) -> dict:
    """Builds the human-readable explanation without ever telling the
    student which event to choose — states facts, offers a consideration."""
    event_a = db.query(Event).filter(Event.id == conflict.event_a_id).first()
    event_b = db.query(Event).filter(Event.id == conflict.event_b_id).first()
    ann_a = db.query(Announcement).filter(Announcement.id == event_a.announcement_id).first() if event_a else None
    ann_b = db.query(Announcement).filter(Announcement.id == event_b.announcement_id).first() if event_b else None

    title_a = (ann_a.title if ann_a else None) or "Event A"
    title_b = (ann_b.title if ann_b else None) or "Event B"

    start_str = conflict.overlap_start.strftime("%I:%M %p") if conflict.overlap_start else "unknown"
    end_str = conflict.overlap_end.strftime("%I:%M %p") if conflict.overlap_end else "unknown"

    explanation = f"'{title_a}' overlaps with '{title_b}' between {start_str} and {end_str}."

    suggestion = None
    if event_a and event_b:
        if event_a.mandatory is True and event_b.mandatory is not True:
            suggestion = f"'{title_a}' is marked mandatory while '{title_b}' is not."
        elif event_b.mandatory is True and event_a.mandatory is not True:
            suggestion = f"'{title_b}' is marked mandatory while '{title_a}' is not."

    return {
        "id": conflict.id,
        "student_id": conflict.student_id,
        "event_a_id": conflict.event_a_id,
        "event_b_id": conflict.event_b_id,
        "event_a_title": title_a,
        "event_b_title": title_b,
        "overlap_start": conflict.overlap_start,
        "overlap_end": conflict.overlap_end,
        "explanation": explanation,
        "suggested_consideration": suggestion,
    }

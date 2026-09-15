from datetime import time
from typing import Optional, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.faculty import Faculty, FacultySchedule
from app.models.timetable import TimetableEntry, Weekday


DAY_ORDER = {
    Weekday.MONDAY: 0,
    Weekday.TUESDAY: 1,
    Weekday.WEDNESDAY: 2,
    Weekday.THURSDAY: 3,
    Weekday.FRIDAY: 4,
    Weekday.SATURDAY: 5,
}


STANDARD_SLOTS = [
    (time(h, 0), time(h + 1, 0))
    for h in range(9, 17)
]


def list_faculty(
    db: Session,
    branch: Optional[str] = None
) -> List[dict]:
    """
    List normalized Faculty records.

    Faculty information comes only from Faculty rows derived
    from existing TimetableEntry data.
    """

    query = db.query(Faculty)

    if branch:
        query = (
            query
            .join(FacultySchedule)
            .join(TimetableEntry)
            .filter(TimetableEntry.branch == branch)
            .distinct()
        )

    faculty_rows = query.order_by(Faculty.name).all()

    result = []

    for faculty in faculty_rows:

        schedules = faculty.schedules

        if branch:
            schedules = [
                s for s in schedules
                if s.timetable_entry.branch == branch
            ]

        subjects = sorted({
            s.timetable_entry.subject_name
            for s in schedules
            if s.timetable_entry.subject_name
        })

        venues = sorted({
            s.timetable_entry.venue
            for s in schedules
            if s.timetable_entry.venue
        })

        branches = sorted({
            s.timetable_entry.branch
            for s in schedules
            if s.timetable_entry.branch
        })

        result.append({
            "name": faculty.name,
            "department": faculty.department,
            "subjects": subjects,
            "venues": venues,
            "branches": branches,
        })

    return result


def search_faculty(
    db: Session,
    query: str
) -> List[Faculty]:
    """
    Case-insensitive partial faculty search.

    Examples:
        shalini
        Shalini
        ARORA
        arora
    """

    pattern = f"%{query.strip().lower()}%"

    return (
        db.query(Faculty)
        .filter(
            func.lower(Faculty.name).like(pattern)
        )
        .order_by(Faculty.name)
        .all()
    )


def find_single_faculty(
    db: Session,
    name: str
) -> Optional[Faculty]:

    exact = (
        db.query(Faculty)
        .filter(
            func.lower(Faculty.name)
            == name.strip().lower()
        )
        .first()
    )

    if exact:
        return exact

    matches = search_faculty(db, name)

    return matches[0] if matches else None


def get_faculty_detail(
    db: Session,
    name: str
) -> Optional[dict]:

    faculty = find_single_faculty(db, name)

    if not faculty:
        return None

    schedules = (
        db.query(FacultySchedule)
        .filter(
            FacultySchedule.faculty_id == faculty.id
        )
        .all()
    )

    subjects = sorted({
        s.timetable_entry.subject_name
        for s in schedules
        if s.timetable_entry.subject_name
    })

    return {
        "name": faculty.name,
        "department": faculty.department,
        "designation": faculty.designation,
        "subjects": subjects,
        "schedule_count": len(schedules),
    }


def get_faculty_timetable(
    db: Session,
    faculty_name: str
) -> Optional[dict]:

    faculty = find_single_faculty(
        db,
        faculty_name
    )

    if not faculty:
        return None

    schedules = (
        db.query(FacultySchedule)
        .filter(
            FacultySchedule.faculty_id == faculty.id
        )
        .all()
    )

    rows = []

    for schedule in schedules:

        entry = schedule.timetable_entry

        rows.append({
            "day": entry.day_of_week.value.capitalize(),
            "start": entry.start_time.strftime("%H:%M"),
            "end": entry.end_time.strftime("%H:%M"),
            "subject_code": entry.subject_code,
            "subject_name": entry.subject_name,
            "branch": entry.branch,
            "year": entry.year,
            "section": (
                schedule.group
                or entry.section
            ),
            "type": (
                "lab"
                if entry.is_lab
                else "lecture"
            ),
            "group": schedule.group,
            "venue": entry.venue,
            "needs_verification": (
                schedule.needs_verification
            ),
        })

    rows.sort(
        key=lambda row: (
            DAY_ORDER[
                Weekday(
                    row["day"].lower()
                )
            ],
            row["start"],
        )
    )

    return {
        "faculty": faculty.name,
        "entries": rows,
    }


def get_faculty_availability(
    db: Session,
    faculty_name: str
) -> Optional[dict]:

    faculty = find_single_faculty(
        db,
        faculty_name
    )

    if not faculty:
        return None

    schedules = (
        db.query(FacultySchedule)
        .filter(
            FacultySchedule.faculty_id == faculty.id
        )
        .all()
    )

    result = {
        "faculty": faculty.name,
        "availability_note": (
            "Availability is calculated only from "
            "the uploaded B.Tech 1st Semester "
            "2026-2027 timetable. It is not "
            "real-time institutional availability."
        ),
    }

    for day in Weekday:

        day_schedules = [
            s for s in schedules
            if s.timetable_entry.day_of_week == day
        ]

        slots = []

        for start, end in STANDARD_SLOTS:

            busy = next(
                (
                    s for s in day_schedules
                    if (
                        s.timetable_entry.start_time < end
                        and
                        s.timetable_entry.end_time > start
                    )
                ),
                None,
            )

            if busy:

                slots.append({
                    "start": start.strftime("%H:%M"),
                    "end": end.strftime("%H:%M"),
                    "status": "busy",
                    "subject": (
                        busy.timetable_entry.subject_name
                    ),
                    "branch": (
                        busy.timetable_entry.branch
                    ),
                    "venue": (
                        busy.timetable_entry.venue
                    ),
                    "group": busy.group,
                })

            else:

                slots.append({
                    "start": start.strftime("%H:%M"),
                    "end": end.strftime("%H:%M"),
                    "status": "free",
                })

        result[
            day.value.capitalize()
        ] = slots

    return result
from typing import Optional, List
from datetime import datetime, time

from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.models.announcement import Announcement
from app.models.timetable import TimetableEntry, Weekday
from app.models.faculty import Faculty, FacultySchedule
from app.services.llm_client import answer_question
from app.config import settings
from app.utils.text_utils import token_set


# ============================================================
# ANNOUNCEMENTS
# ============================================================

def _find_matching_announcements(
    db: Session,
    question: str,
    limit: int = 5,
) -> List[Announcement]:

    words = [w for w in token_set(question) if len(w) > 2]

    if not words:
        return []

    conditions = []

    for word in words:
        pattern = f"%{word}%"

        conditions.extend([
            Announcement.title.ilike(pattern),
            Announcement.description.ilike(pattern),
            Announcement.category.ilike(pattern),
        ])

    return (
        db.query(Announcement)
        .filter(or_(*conditions))
        .order_by(Announcement.submitted_at.desc())
        .limit(limit)
        .all()
    )


def _build_announcement_context(
    announcements: List[Announcement],
) -> str:

    lines = []

    for a in announcements:
        parts = [f"Title: {a.title or 'Untitled'}"]

        if a.event_date:
            parts.append(f"Date: {a.event_date}")

        if a.start_time:
            parts.append(f"Time: {a.start_time}")

        if a.registration_deadline:
            parts.append(
                f"Registration deadline: {a.registration_deadline}"
            )

        if a.location:
            parts.append(f"Location: {a.location}")

        parts.append(
            f"Status: {a.status.value if a.status else 'unknown'}"
        )

        lines.append(" | ".join(parts))

    return "\n".join(lines)


# ============================================================
# FACULTY
# ============================================================

def _find_faculty(
    db: Session,
    question: str,
) -> List[Faculty]:

    # Words like "prof", "professor", "teacher" are NOT names.
    ignored_words = {
        "prof",
        "prof.",
        "professor",
        "teacher",
        "faculty",
        "sir",
        "mam",
        "maam",
        "ma'am",
        "timetable",
        "schedule",
        "show",
        "what",
        "is",
        "the",
        "of",
        "for",
        "please",
        "tell",
        "me",
    }

    words = [
        w.lower().strip(".,?!")
        for w in question.split()
        if len(w.strip(".,?!")) > 2
        and w.lower().strip(".,?!") not in ignored_words
    ]

    if not words:
        return []

    # First try to find faculty using meaningful name words.
    matches = []

    faculty_list = db.query(Faculty).all()

    for faculty in faculty_list:

        faculty_name = faculty.name.lower()

        score = 0

        for word in words:
            if word in faculty_name:
                score += 1

        if score > 0:
            matches.append((score, faculty))

    # Highest name-match score first.
    matches.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        faculty
        for score, faculty in matches[:10]
    ]


def _faculty_schedule(
    db: Session,
    faculty: Faculty,
) -> List[FacultySchedule]:

    return (
        db.query(FacultySchedule)
        .filter(
            FacultySchedule.faculty_id == faculty.id
        )
        .all()
    )


# ============================================================
# TIMETABLE
# ============================================================

DAY_NAMES = {
    "monday": Weekday.MONDAY,
    "tuesday": Weekday.TUESDAY,
    "wednesday": Weekday.WEDNESDAY,
    "thursday": Weekday.THURSDAY,
    "friday": Weekday.FRIDAY,
    "saturday": Weekday.SATURDAY,
}


def _detect_day(question: str) -> Optional[Weekday]:

    q = question.lower()

    for name, day in DAY_NAMES.items():
        if name in q:
            return day

    return None


def _find_timetable_matches(
    db: Session,
    question: str,
    limit: int = 20,
) -> List[TimetableEntry]:

    words = [
        word
        for word in token_set(question)
        if len(word) > 2
    ]

    if not words:
        return []

    conditions = []

    for word in words:
        pattern = f"%{word}%"

        conditions.extend([
            TimetableEntry.subject_name.ilike(pattern),
            TimetableEntry.subject_code.ilike(pattern),
            TimetableEntry.faculty.ilike(pattern),
            TimetableEntry.venue.ilike(pattern),
            TimetableEntry.branch.ilike(pattern),
        ])

    query = db.query(TimetableEntry).filter(
        or_(*conditions)
    )

    day = _detect_day(question)

    if day:
        query = query.filter(
            TimetableEntry.day_of_week == day
        )

    return query.limit(limit).all()


# ============================================================
# INTENT DETECTION
# ============================================================

def _is_faculty_question(question: str) -> bool:

    q = question.lower()

    keywords = [
        "faculty",
        "teacher",
        "professor",
        "prof",
        "sir",
        "ma'am",
        "mam",
        "who teaches",
        "teacher of",
        "taught by",
        "teaches",
    ]

    return any(keyword in q for keyword in keywords)


def _is_availability_question(question: str) -> bool:

    q = question.lower()

    keywords = [
        "available",
        "availability",
        "free",
        "busy",
        "free on",
        "available on",
        "free at",
    ]

    return any(keyword in q for keyword in keywords)


def _is_timetable_question(question: str) -> bool:

    q = question.lower()

    keywords = [
        "timetable",
        "schedule",
        "class",
        "classes",
        "lecture",
        "lab",
        "room",
        "where",
        "when",
        "today",
        "tomorrow",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
    ]

    return any(keyword in q for keyword in keywords)


# ============================================================
# FORMATTERS
# ============================================================

def _format_timetable_entry(
    entry: TimetableEntry,
) -> str:

    day = entry.day_of_week.value.capitalize()

    start = (
        entry.start_time.strftime("%H:%M")
        if hasattr(entry.start_time, "strftime")
        else str(entry.start_time)
    )

    end = (
        entry.end_time.strftime("%H:%M")
        if hasattr(entry.end_time, "strftime")
        else str(entry.end_time)
    )

    subject = entry.subject_name or "Unknown subject"
    room = entry.venue or "Venue not specified"
    faculty = entry.faculty or "Faculty not specified"

    return (
        f"• {day}, {start}–{end} — "
        f"{subject} | Room: {room} | Faculty: {faculty}"
    )


def _format_faculty_timetable(
    faculty: Faculty,
    schedules: List[FacultySchedule],
) -> str:

    if not schedules:
        return (
            f"No timetable entries were found for "
            f"{faculty.name}."
        )

    day_order = {
        Weekday.MONDAY: 0,
        Weekday.TUESDAY: 1,
        Weekday.WEDNESDAY: 2,
        Weekday.THURSDAY: 3,
        Weekday.FRIDAY: 4,
        Weekday.SATURDAY: 5,
    }

    schedules = sorted(
        schedules,
        key=lambda s: (
            day_order.get(
                s.timetable_entry.day_of_week,
                99,
            ),
            s.timetable_entry.start_time,
        ),
    )

    lines = [
        f"Timetable for {faculty.name}:"
    ]

    for schedule in schedules:

        entry = schedule.timetable_entry

        day = entry.day_of_week.value.capitalize()

        start = entry.start_time.strftime("%H:%M")
        end = entry.end_time.strftime("%H:%M")

        group = (
            f" | Group: {schedule.group}"
            if schedule.group
            else ""
        )

        section = (
            f" | Section: {entry.section}"
            if entry.section
            else ""
        )

        lines.append(
            f"• {day}, {start}–{end} — "
            f"{entry.subject_name or 'Unknown subject'}"
            f" | Room: {entry.venue or 'Not specified'}"
            f"{section}{group}"
        )

    return "\n".join(lines)


def _faculty_availability(
    faculty: Faculty,
    schedules: List[FacultySchedule],
    question: str,
) -> str:

    requested_day = _detect_day(question)

    if requested_day:
        schedules = [
            s
            for s in schedules
            if s.timetable_entry.day_of_week
            == requested_day
        ]

        day_name = requested_day.value.capitalize()

        if not schedules:
            return (
                f"According to the uploaded timetable, "
                f"{faculty.name} has no scheduled class on "
                f"{day_name}."
            )

        schedules.sort(
            key=lambda s: s.timetable_entry.start_time
        )

        lines = [
            f"{faculty.name}'s scheduled classes on {day_name}:"
        ]

        for schedule in schedules:

            entry = schedule.timetable_entry

            lines.append(
                f"• {entry.start_time.strftime('%H:%M')}–"
                f"{entry.end_time.strftime('%H:%M')} — "
                f"{entry.subject_name or 'Unknown subject'}"
                f" | Room: {entry.venue or 'Not specified'}"
            )

        lines.append(
            "",
        )

        lines.append(
            "Any time outside these scheduled classes is "
            "not marked as busy by the uploaded timetable."
        )

        return "\n".join(lines)

    return (
        f"I found {len(schedules)} scheduled timetable entries "
        f"for {faculty.name}. Ask for a specific day, such as "
        f"'Is {faculty.name} free on Tuesday?'"
    )


# ============================================================
# MAIN ASK AI FUNCTION
# ============================================================

def ask_campus_ai(
    db: Session,
    question: str,
    student_id: Optional[int] = None,
) -> dict:

    question = question.strip()

    if not question:
        return {
            "answer": "Please ask a campus-related question.",
            "extraction_method": "rule_based",
        }

    # --------------------------------------------------------
    # 1. FACULTY QUESTIONS
    # --------------------------------------------------------

    if _is_faculty_question(question):

        faculty_matches = _find_faculty(db, question)

        if faculty_matches:

            # Faculty availability
            if _is_availability_question(question):

                faculty = faculty_matches[0]

                schedules = _faculty_schedule(
                    db,
                    faculty,
                )

                answer = _faculty_availability(
                    faculty,
                    schedules,
                    question,
                )

                return {
                    "answer": answer,
                    "faculty": faculty.name,
                    "extraction_method": "database",
                }

            # Faculty timetable
            faculty = faculty_matches[0]

            schedules = _faculty_schedule(
                db,
                faculty,
            )

            answer = _format_faculty_timetable(
                faculty,
                schedules,
            )

            return {
                "answer": answer,
                "faculty": faculty.name,
                "extraction_method": "database",
            }

    # --------------------------------------------------------
    # 2. TIMETABLE QUESTIONS
    # --------------------------------------------------------

    if _is_timetable_question(question):

        matches = _find_timetable_matches(
            db,
            question,
        )

        if matches:

            lines = [
                "Here is what I found in the CampusAI timetable:"
            ]

            for entry in matches:
                lines.append(
                    _format_timetable_entry(entry)
                )

            return {
                "answer": "\n".join(lines),
                "matching_timetable_entries": [
                    entry.id
                    for entry in matches
                ],
                "extraction_method": "database",
            }

    # --------------------------------------------------------
    # 3. ANNOUNCEMENTS
    # --------------------------------------------------------

    announcements = _find_matching_announcements(
        db,
        question,
    )

    if announcements:

        context = _build_announcement_context(
            announcements
        )

        if settings.USE_LLM:

            generated = answer_question(
                question,
                context,
            )

            if generated:

                return {
                    "answer": generated,
                    "based_on_announcement_ids": [
                        a.id
                        for a in announcements
                    ],
                    "confidence": (
                        "high"
                        if len(announcements) <= 2
                        else "medium"
                    ),
                    "extraction_method": "llm",
                }

        return {
            "answer": (
                "I found these matching campus announcements:\n\n"
                + "\n".join(
                    f"• {a.title}"
                    for a in announcements
                )
            ),
            "based_on_announcement_ids": [
                a.id
                for a in announcements
            ],
            "extraction_method": "database",
        }

    # --------------------------------------------------------
    # 4. NO MATCH
    # --------------------------------------------------------

    return {
        "answer": (
            "I couldn't find this information in the current "
            "CampusAI campus data. Try asking about your "
            "timetable, a faculty member, faculty availability, "
            "subjects, rooms, or campus announcements."
        ),
        "matching_timetable_entries": [],
        "based_on_announcement_ids": [],
        "extraction_method": "rule_based",
    }
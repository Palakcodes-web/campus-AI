from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.announcement import Announcement
from app.services.llm_client import answer_question
from app.config import settings
from app.utils.text_utils import token_set


def _find_matching_announcements(db: Session, question: str, limit: int = 5) -> List[Announcement]:
    """Naive but dependency-free keyword match — reuses the same token_set
    helper duplicate detection already relies on."""
    words = [w for w in token_set(question) if len(w) > 2]
    if not words:
        return []

    conditions = []
    for w in words:
        pattern = f"%{w}%"
        conditions.append(Announcement.title.ilike(pattern))
        conditions.append(Announcement.description.ilike(pattern))
        conditions.append(Announcement.category.ilike(pattern))

    return (
        db.query(Announcement)
        .filter(or_(*conditions))
        .order_by(Announcement.submitted_at.desc())
        .limit(limit)
        .all()
    )


def _build_context(announcements: List[Announcement]) -> str:
    lines = []
    for a in announcements:
        parts = [f"Title: {a.title or 'Untitled'}"]
        if a.event_date:
            parts.append(f"Date: {a.event_date}")
        if a.start_time:
            parts.append(f"Time: {a.start_time}")
        if a.registration_deadline:
            parts.append(f"Registration deadline: {a.registration_deadline}")
        if a.location:
            parts.append(f"Location: {a.location}")
        parts.append(f"Status: {a.status.value if a.status else 'unknown'}")
        lines.append(" | ".join(parts))
    return "\n".join(lines)


def ask_campus_ai(db: Session, question: str, student_id: Optional[int] = None) -> dict:
    """Deterministic retrieval ALWAYS runs first. LLM (if USE_LLM=true and
    key configured) only generates the phrasing over facts already
    retrieved from the DB — it never gets to invent an answer with no
    matching announcements behind it."""
    matches = _find_matching_announcements(db, question)

    if not matches:
        return {
            "answer": None,
            "based_on_announcement_ids": [],
            "matching_announcements": [],
            "note": "No matching campus announcements were found for this question.",
            "extraction_method": "rule_based",
        }

    if settings.USE_LLM:
        generated = answer_question(question, _build_context(matches))
        if generated:
            return {
                "answer": generated,
                "based_on_announcement_ids": [a.id for a in matches],
                "confidence": "high" if len(matches) <= 2 else "medium",
                "extraction_method": "llm",
            }

    return {
        "answer": None,
        "matching_announcements": [
            {
                "id": a.id,
                "title": a.title,
                "registration_deadline": a.registration_deadline,
                "event_date": a.event_date,
                "status": a.status.value if a.status else None,
            }
            for a in matches
        ],
        "note": "AI unavailable — showing matched announcements instead of a generated answer.",
        "extraction_method": "rule_based",
    }
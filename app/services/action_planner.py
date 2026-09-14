from typing import Optional
from sqlalchemy.orm import Session

from app.models.announcement import Announcement, AnnouncementStatus
from app.models.action import Action


def _build_action_text(ann: Announcement) -> str:
    if ann.status == AnnouncementStatus.CANCELLED:
        return f"Note cancellation: {ann.title or 'Untitled activity'}"
    if ann.registration_required:
        return f"Register for {ann.title or 'this activity'}"
    if ann.status == AnnouncementStatus.UPDATED:
        return f"Review updated details: {ann.title or 'this activity'}"
    return f"Review: {ann.title or 'this activity'}"


def generate_action_for_announcement(db: Session, student_id: int, ann: Announcement) -> Action:
    """One Action row per relevant announcement. Deletes any prior action
    for this (student, announcement) pair first so re-processing doesn't
    duplicate rows."""
    db.query(Action).filter(
        Action.student_id == student_id, Action.announcement_id == ann.id
    ).delete()

    action = Action(
        student_id=student_id,
        announcement_id=ann.id,
        action_text=_build_action_text(ann),
        why_text=ann.why_text,
        deadline=ann.registration_deadline,
        urgency=ann.priority_label.value if ann.priority_label else None,
        missing_info=ann.missing_info or [],
    )
    db.add(action)
    db.commit()
    db.refresh(action)
    return action

from datetime import datetime, timedelta
from typing import Optional, Tuple, List
from app.models.announcement import Announcement, AnnouncementStatus

# Weighted, documented, deterministic. Max raw points sum to 100.
WEIGHTS = {
    "deadline_proximity": 30,
    "event_proximity": 15,
    "mandatory": 15,
    "limited_seats": 10,
    "cancellation_or_update": 15,
    "registration_required": 10,
    "relevance": 5,
}


def _deadline_proximity_score(deadline: Optional[datetime], now: datetime) -> Tuple[int, str]:
    if not deadline:
        return 0, ""
    hours_left = (deadline - now).total_seconds() / 3600
    if hours_left < 0:
        return 0, "deadline has already passed"
    if hours_left <= 6:
        return WEIGHTS["deadline_proximity"], f"registration closes in under 6 hours"
    if hours_left <= 24:
        return int(WEIGHTS["deadline_proximity"] * 0.8), "registration closes within 24 hours"
    if hours_left <= 72:
        return int(WEIGHTS["deadline_proximity"] * 0.5), "registration closes within 3 days"
    return int(WEIGHTS["deadline_proximity"] * 0.2), "registration deadline is more than 3 days away"


def _event_proximity_score(event_date, now: datetime) -> Tuple[int, str]:
    if not event_date:
        return 0, ""
    days_left = (event_date - now.date()).days
    if days_left < 0:
        return 0, "event date has already passed"
    if days_left == 0:
        return WEIGHTS["event_proximity"], "the event is happening today"
    if days_left == 1:
        return int(WEIGHTS["event_proximity"] * 0.8), "the event is happening tomorrow"
    if days_left <= 7:
        return int(WEIGHTS["event_proximity"] * 0.4), "the event is happening this week"
    return 0, ""


def _mandatory_score(mandatory: Optional[bool]) -> Tuple[int, str]:
    if mandatory is True:
        return WEIGHTS["mandatory"], "this activity is mandatory"
    return 0, ""


def _seats_score(seat_limit: Optional[int]) -> Tuple[int, str]:
    if seat_limit is not None and seat_limit <= 50:
        return WEIGHTS["limited_seats"], f"only {seat_limit} seats are available"
    return 0, ""


def _status_score(status: AnnouncementStatus) -> Tuple[int, str]:
    if status == AnnouncementStatus.CANCELLED:
        return WEIGHTS["cancellation_or_update"], "this activity has been cancelled"
    if status == AnnouncementStatus.UPDATED:
        return int(WEIGHTS["cancellation_or_update"] * 0.6), "details of this activity recently changed"
    return 0, ""


def _registration_score(registration_required: Optional[bool]) -> Tuple[int, str]:
    if registration_required is True:
        return WEIGHTS["registration_required"], "registration is required to attend"
    return 0, ""


def _relevance_score(relevance_ratio: float) -> Tuple[int, str]:
    if relevance_ratio >= 0.5:
        return WEIGHTS["relevance"], "it is relevant to your department/interests"
    return 0, ""


def score_to_label(score: int) -> str:
    if score >= 70:
        return "CRITICAL"
    if score >= 50:
        return "HIGH"
    if score >= 25:
        return "MEDIUM"
    return "LOW"


def calculate_priority(
    ann: Announcement,
    now: Optional[datetime] = None,
    relevance_ratio: float = 0.0,
) -> dict:
    """Returns {score, label, why_text, breakdown}. Pure function — every
    input is an already-known field, no LLM call, fully re-derivable and
    inspectable, per the project's 'transparent scoring' requirement."""
    now = now or datetime.utcnow()

    reasons: List[str] = []
    total = 0

    parts = [
        _deadline_proximity_score(ann.registration_deadline, now),
        _event_proximity_score(ann.event_date, now),
        _mandatory_score(ann.mandatory),
        _seats_score(ann.seat_limit),
        _status_score(ann.status),
        _registration_score(ann.registration_required),
        _relevance_score(relevance_ratio),
    ]
    for points, reason in parts:
        total += points
        if reason:
            reasons.append(reason)

    total = max(0, min(100, total))
    label = score_to_label(total)

    if reasons:
        why_text = f"{label.title()} priority because " + ", and ".join(reasons[:3]) + "."
    else:
        why_text = "Low priority — no urgent deadline, mandatory flag, or limited-seat signal detected."

    return {"score": total, "label": label, "why_text": why_text, "breakdown": dict(zip(WEIGHTS.keys(), [p for p, _ in parts]))}
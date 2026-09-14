from datetime import timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.announcement import Announcement, AnnouncementStatus
from app.utils.text_utils import jaccard_similarity

SIMILARITY_DUPLICATE_THRESHOLD = 0.55
SIMILARITY_RELATED_THRESHOLD = 0.30
LOOKBACK_DAYS = 14


def find_candidate_matches(db: Session, new_ann: Announcement):
    """Pull recent, non-superseded announcements in the same category as
    rough candidates for comparison. Keeps this cheap for hackathon scale
    instead of comparing against the whole table."""
    cutoff = new_ann.submitted_at - timedelta(days=LOOKBACK_DAYS) if new_ann.submitted_at else None
    query = db.query(Announcement).filter(
        Announcement.id != new_ann.id,
        Announcement.status != AnnouncementStatus.SUPERSEDED,
    )
    if new_ann.category:
        query = query.filter(Announcement.category == new_ann.category)
    if cutoff:
        query = query.filter(Announcement.submitted_at >= cutoff)
    return query.order_by(Announcement.submitted_at.desc()).all()


def classify_relationship(new_ann: Announcement, existing: Announcement) -> Tuple[str, float]:
    """Returns (relationship, similarity) where relationship is one of:
    'duplicate', 'update', 'cancellation', 'unrelated'.

    Rule order matters: cancellation/update phrases are checked first because
    a short cancellation message ("Python lab cancelled tomorrow") may have
    LOW text similarity to the original but is clearly related by date+category.
    """
    similarity = jaccard_similarity(new_ann.raw_text, existing.raw_text)

    same_date = (
        new_ann.event_date is not None
        and existing.event_date is not None
        and new_ann.event_date == existing.event_date
    )
    likely_related = similarity >= SIMILARITY_RELATED_THRESHOLD or same_date

    if not likely_related:
        return "unrelated", similarity

    if new_ann.status != AnnouncementStatus.CANCELLED and _is_cancellation_text(new_ann):
        return "cancellation", similarity

    if _is_update_text(new_ann) and _fields_changed(new_ann, existing):
        return "update", similarity

    if similarity >= SIMILARITY_DUPLICATE_THRESHOLD:
        return "duplicate", similarity

    return "unrelated", similarity


def _is_cancellation_text(ann: Announcement) -> bool:
    from app.services.extraction import detect_cancellation
    return detect_cancellation(ann.raw_text)


def _is_update_text(ann: Announcement) -> bool:
    from app.services.extraction import detect_update_phrase
    return detect_update_phrase(ann.raw_text)


def _fields_changed(new_ann: Announcement, existing: Announcement) -> bool:
    comparable = ["start_time", "end_time", "location", "event_date"]
    for field in comparable:
        new_val = getattr(new_ann, field)
        old_val = getattr(existing, field)
        if new_val is not None and old_val is not None and new_val != old_val:
            return True
    return False


def find_best_match(db: Session, new_ann: Announcement) -> Optional[Tuple[Announcement, str, float]]:
    """Scans candidates, returns the single best (existing, relationship,
    similarity) tuple, preferring the highest similarity among related
    matches. Returns None if nothing is related."""
    candidates = find_candidate_matches(db, new_ann)
    best = None
    for existing in candidates:
        relationship, similarity = classify_relationship(new_ann, existing)
        if relationship == "unrelated":
            continue
        if best is None or similarity > best[2]:
            best = (existing, relationship, similarity)
    return best
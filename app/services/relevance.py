from typing import Optional
from app.models.student import Student
from app.models.announcement import Announcement
from app.utils.text_utils import token_set


def calculate_relevance(student: Optional[Student], ann: Announcement) -> float:
    """Returns a 0.0–1.0 relevance ratio. Never fabricates a connection —
    if the announcement doesn't mention the student's department/interests/
    year at all, relevance is 0."""
    if not student:
        return 0.0

    haystack = token_set(f"{ann.title or ''} {ann.description or ''} {ann.category or ''}")
    if not haystack:
        return 0.0

    signals = 0
    matched = 0

    if student.department:
        signals += 1
        if token_set(student.department) & haystack:
            matched += 1

    if student.interests:
        signals += 1
        interest_tokens = set()
        for interest in student.interests:
            interest_tokens |= token_set(interest)
        if interest_tokens & haystack:
            matched += 1

    if student.year:
        signals += 1
        year_words = {"first-year", "1st", "freshers", "fresher"} if student.year == 1 else set()
        if year_words & haystack:
            matched += 1

    if signals == 0:
        return 0.0
    return matched / signals

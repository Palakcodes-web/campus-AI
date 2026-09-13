import re
from datetime import datetime, date, time, timedelta
from dateutil import parser as dtparser
from typing import Optional, Dict, Any, List

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

CATEGORY_KEYWORDS = {
    "exam": ["exam", "examination", "midterm", "endsem", "end-sem"],
    "scholarship": ["scholarship", "fee waiver", "financial aid"],
    "internship": ["internship", "intern "],
    "placement": ["placement", "recruitment drive", "campus hiring", "interview shortlist"],
    "workshop": ["workshop", "bootcamp", "hands-on session", "training session"],
    "timetable": ["timetable", "schedule change", "class shifted", "lab shifted", "rescheduled class"],
    "club/society": ["club", "society", "chapter meeting"],
    "hostel": ["hostel", "mess", "warden", "room allotment"],
    "administrative": ["fee payment", "id card", "circular", "notice from admin", "office order"],
    "opportunity": ["hackathon", "competition", "fellowship", "call for applications"],
    "event": ["fest", "seminar", "webinar", "guest lecture", "cultural event", "sports event"],
    "academic": ["lab", "assignment", "project submission", "class", "lecture"],
}

CANCEL_KEYWORDS = ["cancelled", "canceled", "called off", "stands cancelled", "no longer happening"]
UPDATE_KEYWORDS = ["shifted to", "rescheduled to", "moved to", "changed to", "now at",
                    "postponed to", "new time", "revised time", "extended to"]
MANDATORY_KEYWORDS = ["mandatory", "compulsory", "must attend"]
OPTIONAL_KEYWORDS = ["optional", "not compulsory"]
REGISTRATION_KEYWORDS = ["register", "registration", "sign up", "apply", "rsvp"]

TIME_PATTERN = re.compile(
    r"(\d{1,2}(?::\d{2})?\s*(?:am|pm))", re.IGNORECASE
)
SEAT_PATTERN = re.compile(
    r"(?:only\s+)?(\d{1,4})\s*(?:seats?|slots?|spots?)", re.IGNORECASE
)
DATE_KEYWORD_PATTERN = re.compile(
    r"\b(today|tomorrow|day after tomorrow|" + "|".join(WEEKDAYS) + r")\b", re.IGNORECASE
)
EXPLICIT_DATE_PATTERN = re.compile(
    r"\b(\d{1,2}(?:st|nd|rd|th)?\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*"
    r"|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?)"
    r"(?:\s*,?\s*\d{4})?\b",
    re.IGNORECASE,
)
DEADLINE_TRIGGER_PATTERN = re.compile(
    r"(?:register|apply|submit|deadline|last date|last chance|closes?)\s*(?:before|by|on|:)?\s*"
    r"([a-z0-9:.\s]+?)(?:\.|,|$)",
    re.IGNORECASE,
)
TONIGHT_PATTERN = re.compile(r"\btonight\b", re.IGNORECASE)


def _parse_time_str(s: str) -> Optional[time]:
    try:
        return dtparser.parse(s).time()
    except (ValueError, OverflowError):
        return None


def _resolve_keyword_date(keyword: str, reference: date) -> Optional[date]:
    keyword = keyword.lower()
    if keyword == "today":
        return reference
    if keyword == "tomorrow":
        return reference + timedelta(days=1)
    if keyword == "day after tomorrow":
        return reference + timedelta(days=2)
    if keyword in WEEKDAYS:
        target_idx = WEEKDAYS.index(keyword)
        days_ahead = (target_idx - reference.weekday()) % 7
        days_ahead = days_ahead or 7  # next occurrence, not today
        return reference + timedelta(days=days_ahead)
    return None


def extract_category(text: str) -> Optional[str]:
    lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in lower:
                return category
    return None


def extract_title(text: str) -> str:
    """Best-effort short title: strip urgency punctuation/filler, take a
    leading clause. Never invents content beyond what's in the raw text."""
    cleaned = re.sub(r"!{1,}", "", text)
    cleaned = re.sub(r"^\s*(guys|urgent|reminder|hey|hi|fyi)[:,]?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip()
    # cut at first strong delimiter to avoid dragging in trailing deadline clauses
    for delim in [". ", " - ", " – "]:
        if delim in cleaned:
            cleaned = cleaned.split(delim)[0]
            break
    words = cleaned.split()
    title = " ".join(words[:12]).strip(" .,:;")
    return title if title else text[:60].strip()


def extract_event_date(text: str, reference_dt: datetime) -> Optional[date]:
    m = DATE_KEYWORD_PATTERN.search(text)
    if m:
        resolved = _resolve_keyword_date(m.group(1), reference_dt.date())
        if resolved:
            return resolved
    m = EXPLICIT_DATE_PATTERN.search(text)
    if m:
        try:
            parsed = dtparser.parse(m.group(0), default=reference_dt, fuzzy=True)
            return parsed.date()
        except (ValueError, OverflowError):
            return None
    return None


def extract_time_range(text: str):
    """Returns (start_time, end_time) — either may be None if not stated.
    If an update phrase like 'shifted to 5 PM' exists, that time wins as the
    (new) start time."""
    times = TIME_PATTERN.findall(text)
    start_time, end_time = None, None

    for phrase in UPDATE_KEYWORDS:
        idx = text.lower().find(phrase)
        if idx != -1:
            after = text[idx: idx + len(phrase) + 15]
            m = TIME_PATTERN.search(after)
            if m:
                start_time = _parse_time_str(m.group(1))
                return start_time, end_time

    if len(times) >= 2:
        start_time = _parse_time_str(times[0])
        end_time = _parse_time_str(times[1])
    elif len(times) == 1:
        start_time = _parse_time_str(times[0])

    return start_time, end_time


def extract_seat_limit(text: str) -> Optional[int]:
    m = SEAT_PATTERN.search(text)
    if m:
        return int(m.group(1))
    return None


def extract_deadline(text: str, reference_dt: datetime) -> Optional[datetime]:
    if TONIGHT_PATTERN.search(text):
        return reference_dt.replace(hour=23, minute=59, second=0, microsecond=0)

    m = DEADLINE_TRIGGER_PATTERN.search(text)
    if not m:
        return None
    candidate = m.group(1).strip()
    if not candidate:
        return None

    date_kw = DATE_KEYWORD_PATTERN.search(candidate)
    time_m = TIME_PATTERN.search(candidate)
    explicit_date_m = EXPLICIT_DATE_PATTERN.search(candidate)

    result_date = reference_dt.date()
    if date_kw:
        resolved = _resolve_keyword_date(date_kw.group(1), reference_dt.date())
        if resolved:
            result_date = resolved
    elif explicit_date_m:
        try:
            result_date = dtparser.parse(explicit_date_m.group(0), default=reference_dt, fuzzy=True).date()
        except (ValueError, OverflowError):
            pass
    else:
        return None  # no recognizable date signal — do not invent one

    result_time = time(23, 59) if not time_m else (_parse_time_str(time_m.group(1)) or time(23, 59))
    return datetime.combine(result_date, result_time)


def detect_cancellation(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in CANCEL_KEYWORDS)


def detect_update_phrase(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in UPDATE_KEYWORDS)


def detect_mandatory(text: str) -> Optional[bool]:
    lower = text.lower()
    if any(kw in lower for kw in MANDATORY_KEYWORDS):
        return True
    if any(kw in lower for kw in OPTIONAL_KEYWORDS):
        return False
    return None  # unknown — do not guess


def detect_registration_required(text: str) -> Optional[bool]:
    lower = text.lower()
    if any(kw in lower for kw in REGISTRATION_KEYWORDS):
        return True
    return None


def extract_location(text: str) -> Optional[str]:
    m = re.search(r"\bin\s+([A-Z][A-Za-z0-9\s\-]{2,30})", text)
    if m:
        return m.group(1).strip(" .,")
    m = re.search(r"\bat\s+((?:block|room|hall|auditorium|lab)\s*[A-Za-z0-9\-]*)", text, re.IGNORECASE)
    if m:
        return m.group(1).strip(" .,")
    return None


def extract_organizer(text: str) -> Optional[str]:
    m = re.search(r"\bby\s+([A-Z][A-Za-z0-9&\s]{2,40})", text)
    if m:
        return m.group(1).strip(" .,")
    return None


def rule_based_extract(raw_text: str, reference_dt: Optional[datetime] = None) -> Dict[str, Any]:
    """Deterministic extraction. Every field is None/False/unknown unless the
    text actually supports it — this is the fallback path and must never
    depend on the LLM being available."""
    reference_dt = reference_dt or datetime.utcnow()

    is_cancelled = detect_cancellation(raw_text)
    start_time, end_time = extract_time_range(raw_text)

    fields: Dict[str, Any] = {
        "title": extract_title(raw_text),
        "description": raw_text,
        "category": extract_category(raw_text),
        "location": extract_location(raw_text),
        "organizer": extract_organizer(raw_text),
        "event_date": extract_event_date(raw_text, reference_dt),
        "start_time": start_time,
        "end_time": end_time,
        "registration_deadline": extract_deadline(raw_text, reference_dt),
        "seat_limit": extract_seat_limit(raw_text),
        "registration_required": detect_registration_required(raw_text),
        "mandatory": detect_mandatory(raw_text),
        "is_cancelled": is_cancelled,
        "is_update_phrase": detect_update_phrase(raw_text),
        "extraction_method": "rule_based",
    }

    missing_info: List[str] = []
    if fields["event_date"] and not fields["location"]:
        missing_info.append("location")
    if fields["event_date"] and not fields["end_time"] and fields["start_time"]:
        missing_info.append("end_time")
    if fields["registration_required"] and not fields["registration_deadline"]:
        missing_info.append("registration_deadline")
    if not fields["category"]:
        missing_info.append("category")
    fields["missing_info"] = missing_info

    known_fields = [
        fields["title"], fields["category"], fields["event_date"],
        fields["start_time"], fields["location"], fields["organizer"],
    ]
    fields["confidence_score"] = round(sum(1 for f in known_fields if f) / len(known_fields), 2)

    return fields
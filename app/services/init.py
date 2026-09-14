import re


def normalize_text(text: str) -> str:
    """Lowercase, strip filler/urgency noise, collapse whitespace. Used for
    comparison/matching only — never overwrites the original raw_text."""
    t = text.lower()
    t = re.sub(r"!{1,}", " ", t)
    t = re.sub(r"\b(guys|urgent|reminder|hey|hi|fyi|please note|note[:]?)\b", " ", t)
    t = re.sub(r"[^a-z0-9\s:/\-]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def token_set(text: str) -> set:
    return set(normalize_text(text).split())


def jaccard_similarity(a: str, b: str) -> float:
    """Simple, dependency-free token-overlap similarity in [0, 1]."""
    sa, sb = token_set(a), token_set(b)
    if not sa or not sb:
        return 0.0
    intersection = len(sa & sb)
    union = len(sa | sb)
    return intersection / union if union else 0.

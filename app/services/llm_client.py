import json
from datetime import datetime
from typing import Optional, Dict, Any

from app.config import settings
from app.services.extraction import rule_based_extract

_client = None
if settings.USE_LLM and settings.OPENAI_API_KEY:
    try:
        from openai import OpenAI
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    except Exception:
        _client = None

EXTRACTION_PROMPT = """You extract structured fields from a messy campus announcement.
Return ONLY a compact JSON object with these keys (use null for anything not
stated in the text — NEVER invent or guess a value):

title, description, category, location, organizer, event_date (YYYY-MM-DD or null),
start_time (HH:MM 24hr or null), end_time (HH:MM 24hr or null),
registration_deadline (YYYY-MM-DD HH:MM or null), seat_limit (integer or null),
registration_required (true/false/null), mandatory (true/false/null),
is_cancelled (true/false), is_update_phrase (true/false)

Reference datetime for resolving relative dates like "tomorrow": {reference}

Announcement:
\"\"\"{text}\"\"\"

JSON only, no explanation, no markdown fences.
"""


def _parse_llm_json(raw: str) -> Optional[Dict[str, Any]]:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json\n", "", 1).replace("json", "", 1)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def llm_extract(raw_text: str, reference_dt: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
    """Attempts LLM extraction. Returns None on ANY failure so the caller
    can fall back to rule_based_extract — this function must never raise."""
    if _client is None:
        return None
    reference_dt = reference_dt or datetime.utcnow()
    try:
        response = _client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": EXTRACTION_PROMPT.format(
                reference=reference_dt.isoformat(), text=raw_text
            )}],
            temperature=0,
            timeout=8,
        )
        content = response.choices[0].message.content
        parsed = _parse_llm_json(content)
        if not parsed:
            return None
        parsed["extraction_method"] = "llm"
        return parsed
    except Exception:
        return None


def extract_information(raw_text: str, reference_dt: Optional[datetime] = None) -> Dict[str, Any]:
    """Hybrid entry point: rule-based ALWAYS runs first (source of truth for
    dates/deadlines/math). LLM result, if available and valid, only fills
    fields the rule-based pass left as None — it never overrides a
    rule-based value, per the project's deterministic-first rule."""
    reference_dt = reference_dt or datetime.utcnow()
    base = rule_based_extract(raw_text, reference_dt)

    if not settings.USE_LLM:
        return base

    llm_result = llm_extract(raw_text, reference_dt)
    if not llm_result:
        return base

    merged = dict(base)
    fillable = ["title", "description", "category", "location", "organizer"]
    for key in fillable:
        if not merged.get(key) and llm_result.get(key):
            merged[key] = llm_result[key]

    merged["extraction_method"] = "hybrid"
    merged["confidence_score"] = min(1.0, round((merged.get("confidence_score") or 0) + 0.15, 2))
    return merged
   

def answer_question(question: str, context_text: str) -> Optional[str]:
    """Answers a free-text question using ONLY the given context text.
    Returns None on any failure so the caller falls back to a
    non-generated response — reuses the same _client instance set up
    above, no new OpenAI configuration."""
    if _client is None:
        return None
    try:
        response = _client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": (
                "Answer the student's question using ONLY the campus announcement "
                "information given below. If the answer isn't in the information, "
                "say you don't have that information. Never invent details.\n\n"
                f"Campus announcement information:\n{context_text}\n\n"
                f"Question: {question}\n\nAnswer concisely."
            )}],
            temperature=0,
            timeout=8,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.announcement import Announcement
from app.models.student import Student
from app.services.relevance import calculate_relevance

router = APIRouter(prefix="/api", tags=["search"])


@router.get("/search")
def search_announcements(
    q: str = Query(..., min_length=2),
    category: Optional[str] = None,
    student_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    like_pattern = f"%{q}%"
    query = db.query(Announcement).filter(
        (Announcement.title.ilike(like_pattern))
        | (Announcement.description.ilike(like_pattern))
        | (Announcement.category.ilike(like_pattern))
    )
    if category:
        query = query.filter(Announcement.category == category)

    results = query.order_by(Announcement.submitted_at.desc()).limit(50).all()

    if student_id is not None:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        results = sorted(results, key=lambda a: calculate_relevance(student, a), reverse=True)

    return {
        "query": q,
        "results": [
            {
                "id": a.id,
                "title": a.title,
                "category": a.category,
                "event_date": a.event_date,
                "start_time": a.start_time,
                "location": a.location,
                "status": a.status.value if a.status else None,
                "priority_label": a.priority_label.value if a.priority_label else None,
                "confidence_score": a.confidence_score,
            }
            for a in results
        ],
        "count": len(results),
    }
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from app.database import Base


class Conflict(Base):
    __tablename__ = "conflicts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    event_a_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    event_b_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    overlap_start = Column(DateTime(timezone=True), nullable=True)
    overlap_end = Column(DateTime(timezone=True), nullable=True)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
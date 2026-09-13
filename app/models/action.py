from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, func
from app.database import Base


class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    announcement_id = Column(Integer, ForeignKey("announcements.id"), nullable=False)
    action_text = Column(String, nullable=False)
    why_text = Column(Text, nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    urgency = Column(String, nullable=True)
    missing_info = Column(JSON, nullable=True, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
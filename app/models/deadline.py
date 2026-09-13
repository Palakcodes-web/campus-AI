from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base


class Deadline(Base):
    __tablename__ = "deadlines"

    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(Integer, ForeignKey("announcements.id"), nullable=False)
    deadline_datetime = Column(DateTime(timezone=True), nullable=False, index=True)
    description = Column(String, nullable=True)
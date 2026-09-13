from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey
from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(Integer, ForeignKey("announcements.id"), unique=True, nullable=False)
    title = Column(String, nullable=True)
    event_date = Column(Date, nullable=True, index=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    mandatory = Column(Boolean, nullable=True, default=None)
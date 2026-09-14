import enum
from sqlalchemy import Column, Integer, String, Time, Boolean, DateTime, ForeignKey, Enum, func
from app.database import Base


class Weekday(str, enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"


class TimetableEntry(Base):
    __tablename__ = "timetable_entries"

    id = Column(Integer, primary_key=True, index=True)
    branch = Column(String, nullable=False, index=True)          # e.g. "CSE", "Robotics and AI"
    year = Column(Integer, nullable=False, index=True)
    section = Column(String, nullable=True)                       # e.g. "C1" — null = applies to whole class
    day_of_week = Column(Enum(Weekday), nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    subject_code = Column(String, nullable=True)
    subject_name = Column(String, nullable=False)
    faculty = Column(String, nullable=True)
    venue = Column(String, nullable=True)
    is_lab = Column(Boolean, nullable=True, default=False)
    mandatory = Column(Boolean, nullable=True, default=True)


class TimetableConflict(Base):
    __tablename__ = "timetable_conflicts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    timetable_entry_id = Column(Integer, ForeignKey("timetable_entries.id"), nullable=False)
    overlap_start = Column(DateTime(timezone=True), nullable=True)
    overlap_end = Column(DateTime(timezone=True), nullable=True)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
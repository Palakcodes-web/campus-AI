from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Faculty(Base):
    """Normalized faculty identity — derived from the faculty strings
    already present in existing, verified TimetableEntry rows. No new
    names/departments are invented here; department/designation are left
    null unless explicitly known."""
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    department = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    schedules = relationship("FacultySchedule", back_populates="faculty")


class FacultySchedule(Base):
    """Links a Faculty to an existing TimetableEntry. Multiple rows can
    point to the same timetable_entry_id (one per co-teaching faculty),
    which is how 'both faculty members must receive that entry' is
    satisfied without duplicating the TimetableEntry itself."""
    __tablename__ = "faculty_schedules"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False, index=True)
    timetable_entry_id = Column(Integer, ForeignKey("timetable_entries.id"), nullable=False, index=True)
    group = Column(String, nullable=True)  # e.g. "C1", "GP2" — only when the source text ties THIS faculty to a specific group
    needs_verification = Column(Boolean, nullable=False, default=False)

    faculty = relationship("Faculty", back_populates="schedules")
    timetable_entry = relationship("TimetableEntry")
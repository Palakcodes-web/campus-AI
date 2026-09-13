import enum
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float, DateTime, Date, Time,
    ForeignKey, Enum, JSON, func
)
from sqlalchemy.orm import relationship
from app.database import Base


class AnnouncementStatus(str, enum.Enum):
    NEW = "new"
    UPDATED = "updated"
    CANCELLED = "cancelled"
    SUPERSEDED = "superseded"


class ExtractionMethod(str, enum.Enum):
    RULE_BASED = "rule_based"
    LLM = "llm"
    HYBRID = "hybrid"


class PriorityLabel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)

    raw_text = Column(Text, nullable=False)
    source = Column(String, nullable=True)
    sender = Column(String, nullable=True)
    category = Column(String, nullable=True, index=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    organizer = Column(String, nullable=True)

    event_date = Column(Date, nullable=True, index=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    registration_deadline = Column(DateTime(timezone=True), nullable=True)

    seat_limit = Column(Integer, nullable=True)
    registration_required = Column(Boolean, nullable=True, default=None)
    mandatory = Column(Boolean, nullable=True, default=None)

    status = Column(Enum(AnnouncementStatus), default=AnnouncementStatus.NEW, index=True)
    duplicate_of_id = Column(Integer, ForeignKey("announcements.id"), nullable=True)

    priority_score = Column(Integer, nullable=True)
    priority_label = Column(Enum(PriorityLabel), nullable=True)
    why_text = Column(Text, nullable=True)
    missing_info = Column(JSON, nullable=True, default=list)  # list[str]

    confidence_score = Column(Float, nullable=True)
    extraction_method = Column(Enum(ExtractionMethod), nullable=True)

    processed = Column(Boolean, default=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    versions = relationship(
        "AnnouncementVersion", back_populates="announcement", cascade="all, delete-orphan"
    )
    duplicate_of = relationship("Announcement", remote_side=[id])


class AnnouncementVersion(Base):
    __tablename__ = "announcement_versions"

    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(Integer, ForeignKey("announcements.id"), nullable=False)
    raw_text = Column(Text, nullable=False)
    changed_fields = Column(JSON, nullable=True)  # dict of field -> {old, new}
    version_number = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    announcement = relationship("Announcement", back_populates="versions")
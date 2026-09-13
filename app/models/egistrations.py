from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class StudentRegistration(Base):
    __tablename__ = "student_registrations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    announcement_id = Column(Integer, ForeignKey("announcements.id"), nullable=False)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="registrations")
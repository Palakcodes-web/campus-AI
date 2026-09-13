from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    semester = Column(Integer, nullable=True)
    interests = Column(JSON, nullable=True, default=list)  # list[str]
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    registrations = relationship("StudentRegistration", back_populates="student")
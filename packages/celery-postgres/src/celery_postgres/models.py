from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .connection import Base


class Job(Base):
    """Job 테이블 - Celery task 실행 정보."""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(255), unique=True, index=True, nullable=False)
    status = Column(String(50), default="PENDING", nullable=False)  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    steps = relationship("JobStep", back_populates="job", cascade="all, delete-orphan")


class JobStep(Base):
    """JobStep 테이블 - 각 작업의 단계별 진행 상황."""

    __tablename__ = "job_steps"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, nullable=False)  # 1, 2, 3
    status = Column(String(50), default="PENDING", nullable=False)  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationship
    job = relationship("Job", back_populates="steps")

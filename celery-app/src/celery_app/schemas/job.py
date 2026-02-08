from datetime import datetime
from pydantic import BaseModel


class JobStepResponse(BaseModel):
    """JobStep 응답 스키마."""

    id: int
    step_number: int
    status: str
    message: str | None
    started_at: datetime | None
    completed_at: datetime | None

    class Config:
        from_attributes = True


class JobResponse(BaseModel):
    """Job 응답 스키마."""

    id: int
    task_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    steps: list[JobStepResponse]

    class Config:
        from_attributes = True


class JobCreateResponse(BaseModel):
    """Job 생성 응답 스키마."""

    job_id: int
    task_id: str
    status: str
    message: str

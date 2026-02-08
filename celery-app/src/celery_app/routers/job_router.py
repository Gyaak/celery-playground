from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from celery import Celery
from celery_app.services import JobService
from celery_app.schemas import JobResponse, JobCreateResponse
from celery_app.dependency import get_celery_app
from celery_postgres import get_sync_session


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobCreateResponse, status_code=201)
def create_job(
    celery_app: Celery = Depends(get_celery_app),
    session: Session = Depends(get_sync_session),
):
    """
    새 Job을 생성하고 Celery task를 시작합니다.
    """
    service = JobService(session, celery_app)
    job, task_id = service.create_and_submit_job()

    return JobCreateResponse(
        job_id=job.id,
        task_id=task_id,
        status=job.status,
        message="Job created and submitted successfully",
    )


@router.get("", response_model=list[JobResponse])
def get_jobs(
    status: str | None = None,
    session: Session = Depends(get_sync_session),
    celery_app: Celery = Depends(get_celery_app),
):
    """
    모든 Job 목록을 조회합니다.
    status 파라미터로 필터링 가능 (PENDING, IN_PROGRESS, COMPLETED, FAILED).
    """
    service = JobService(session, celery_app)

    if status:
        jobs = service.get_jobs_by_status(status)
    else:
        jobs = service.get_all_jobs()

    return [JobResponse.model_validate(job) for job in jobs]


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    session: Session = Depends(get_sync_session),
    celery_app: Celery = Depends(get_celery_app),
):
    """
    특정 Job의 상세 정보를 조회합니다.
    """
    service = JobService(session, celery_app)
    job = service.get_job_by_id(job_id)

    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    return JobResponse.model_validate(job)

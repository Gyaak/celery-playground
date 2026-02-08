import uuid
from celery import Celery
from sqlalchemy.orm import Session

from celery_postgres import Job
from celery_tasks import TaskNames
from celery_app.repositories import JobRepository


class JobService:
    """Job 비즈니스 로직을 처리하는 Service."""

    def __init__(self, session: Session, celery_app: Celery):
        self.repository = JobRepository(session)
        self.celery_app = celery_app

    def create_and_submit_job(self) -> tuple[Job, str]:
        """
        새 Job을 생성하고 Celery task를 제출.

        Returns:
            tuple[Job, str]: 생성된 Job과 task_id
        """
        # 임시 task_id로 Job 생성 (UUID 사용)
        job = self.repository.create_job(task_id=f"pending-{uuid.uuid4()}")

        # Celery task 제출 (Worker가 실행하면서 Step을 생성함)
        task = self.celery_app.send_task(TaskNames.PROCESS_JOB, args=[job.id])

        # 실제 task_id로 업데이트
        job.task_id = task.id
        self.repository.session.commit()
        self.repository.session.refresh(job)

        return job, task.id

    def get_all_jobs(self) -> list[Job]:
        """모든 Job 조회."""
        return self.repository.get_all_jobs()

    def get_job_by_id(self, job_id: int) -> Job | None:
        """ID로 Job 조회."""
        return self.repository.get_job_by_id(job_id)

    def get_jobs_by_status(self, status: str) -> list[Job]:
        """특정 상태의 Job 조회."""
        return self.repository.get_jobs_by_status(status)

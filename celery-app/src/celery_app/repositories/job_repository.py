from sqlalchemy.orm import Session, joinedload
from celery_postgres import Job, JobStep


class JobRepository:
    """Job 데이터베이스 작업을 처리하는 Repository."""

    def __init__(self, session: Session):
        self.session = session

    def create_job(self, task_id: str) -> Job:
        """새 Job 생성."""
        job = Job(task_id=task_id, status="PENDING")
        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job

    def create_job_steps(self, job_id: int) -> list[JobStep]:
        """Job에 대한 3개의 초기 JobStep 생성."""
        steps = []
        for step_num in range(1, 4):
            step = JobStep(
                job_id=job_id,
                step_number=step_num,
                status="PENDING",
                message=f"Step {step_num} waiting to be processed",
            )
            self.session.add(step)
            steps.append(step)

        self.session.commit()
        return steps

    def get_job_by_id(self, job_id: int) -> Job | None:
        """ID로 Job 조회 (steps 포함)."""
        return (
            self.session.query(Job)
            .options(joinedload(Job.steps))
            .filter(Job.id == job_id)
            .first()
        )

    def get_all_jobs(self) -> list[Job]:
        """모든 Job 조회 (steps 포함)."""
        return self.session.query(Job).options(joinedload(Job.steps)).all()

    def get_jobs_by_status(self, status: str) -> list[Job]:
        """특정 상태의 Job 조회 (steps 포함)."""
        return (
            self.session.query(Job)
            .options(joinedload(Job.steps))
            .filter(Job.status == status)
            .all()
        )

import time
from datetime import datetime
from celery import Celery, Task
from celery_postgres import get_sync_session_context, Job, JobStep
from celery_tasks import TaskNames


def register_process_job_task(celery_app: Celery):
    """Process Job Task를 Celery 앱에 등록하는 함수."""

    @celery_app.task(bind=True, name=TaskNames.PROCESS_JOB)
    def process_job(self: Task, job_id: int):
        """
        3단계로 Job을 처리하는 Celery Task.
        각 단계마다 print + sleep 5초 + DB 업데이트.
        """
        task_id = self.request.id
        print(f"[Task {task_id}] Starting job processing for job_id={job_id}")

        with get_sync_session_context() as session:
            # Job 상태를 IN_PROGRESS로 업데이트
            job = session.query(Job).filter(Job.id == job_id).first()
            if not job:
                print(f"[Task {task_id}] Job {job_id} not found")
                return {"status": "FAILED", "message": "Job not found"}

            job.status = "IN_PROGRESS"
            session.commit()

            try:
                # 3단계 처리
                for step_num in range(1, 4):
                    print(f"[Task {task_id}] Step {step_num} started for job_id={job_id}")

                    # Step 시작 시점에 IN_PROGRESS로 생성
                    step = JobStep(
                        job_id=job_id,
                        step_number=step_num,
                        status="IN_PROGRESS",
                        started_at=datetime.now(),
                        message=f"Processing step {step_num}",
                    )
                    session.add(step)
                    session.commit()

                    # 더미 작업: print + sleep 5초
                    print(f"[Task {task_id}] Step {step_num} processing... (sleeping 5 seconds)")
                    time.sleep(5)

                    # Step 성공 처리
                    step.status = "COMPLETED"
                    step.completed_at = datetime.now()
                    step.message = f"Step {step_num} completed successfully"
                    session.commit()

                    print(f"[Task {task_id}] Step {step_num} completed for job_id={job_id}")

                # Job 완료 처리
                job.status = "COMPLETED"
                job.updated_at = datetime.now()
                session.commit()

                print(f"[Task {task_id}] Job {job_id} processing completed")

                return {
                    "status": "COMPLETED",
                    "job_id": job_id,
                    "task_id": task_id,
                    "message": "Job processed successfully",
                }

            except Exception as e:
                # Job 실패 처리
                job.status = "FAILED"
                job.updated_at = datetime.now()
                session.commit()

                print(f"[Task {task_id}] Job {job_id} failed: {e}")

                return {
                    "status": "FAILED",
                    "job_id": job_id,
                    "task_id": task_id,
                    "message": f"Job failed: {str(e)}",
                }

    return process_job

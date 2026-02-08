from celery_tasks import create_celery_app
from celery_redis import redis_settings
from celery_postgres import db_settings
from celery_worker.tasks import register_process_job_task


app = create_celery_app(
    name="celery_worker",
    broker_url=redis_settings.redis_url,
    backend_url=db_settings.celery_backend_url,
)

# Task 등록
process_job = register_process_job_task(app)

"""Celery Worker 실행 진입점."""

from celery_worker.celery_app import app

if __name__ == "__main__":
    # Celery worker 실행
    argv = ["worker", "--loglevel=info"]
    app.worker_main(argv)

"""공통 Celery 앱 설정."""

from celery import Celery


def create_celery_app(
    name: str,
    broker_url: str,
    backend_url: str,
) -> Celery:
    """
    Celery 앱을 생성하는 팩토리 함수.

    Args:
        name: Celery 앱 이름
        broker_url: Celery 브로커 URL (예: redis://localhost:6379/0)
        backend_url: Celery 백엔드 URL (예: db+postgresql://user:pass@localhost:5432/db)

    Returns:
        설정된 Celery 앱 인스턴스
    """
    app = Celery(
        name,
        broker=broker_url,
        backend=backend_url,
    )

    # Celery 설정
    app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,  # 30분
        task_soft_time_limit=25 * 60,  # 25분
    )

    return app

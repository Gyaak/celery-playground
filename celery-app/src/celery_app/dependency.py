from celery import Celery

from celery_tasks import create_celery_app
from celery_redis import redis_settings


def get_celery_app() -> Celery:
    """Celery 앱 의존성 - FastAPI에서 사용하는 Celery 클라이언트."""
    # API는 task를 보내기만 하므로 backend는 필요 없음
    return create_celery_app(
        name="celery_client",
        broker_url=redis_settings.redis_url,
        backend_url="",  # No backend needed for API
    )

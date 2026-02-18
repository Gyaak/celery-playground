# 모든 practice에서 공유하는 인프라 접속 정보
# docker-compose.yml 의 서비스 설정과 대응됨

REDIS_URL    = "redis://localhost:6379"
RABBITMQ_URL = "amqp://localhost:5672"
POSTGRES_URL = "db+postgresql://postgres:postgres@localhost:5432/celery_jobs"

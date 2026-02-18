import os

import billiard
from celery import Celery

from global_config import *

# macOS에서 prefork worker가 정상 동작하도록 기본 방식을 spawn으로 고정
billiard.context._force_start_method('spawn')
os.environ['FORKED_BY_MULTIPROCESSING'] = '1'

app = Celery(
    'practice03',
    broker=RABBITMQ_URL,
    # chord 완료 감지를 위해 Redis 사용
    # Redis: atomic INCR 카운터 방식으로 즉시 감지
    # PostgreSQL: chord_unlock 폴링 방식으로 최대 1초 지연 발생
    backend=REDIS_URL,
    # backend=POSTGRES_URL,
)

app.conf.update(
    worker_concurrency=4,  # 동시에 실행할 worker 프로세스 수
    worker_pool='prefork', # 멀티프로세싱 기반 실행 풀
)

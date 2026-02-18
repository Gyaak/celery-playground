import os

import billiard
from celery import Celery

from global_config import RABBITMQ_URL, POSTGRES_URL

# macOS에서 prefork worker가 정상 동작하도록 기본 방식을 spawn으로 고정
billiard.context._force_start_method('spawn')
os.environ['FORKED_BY_MULTIPROCESSING'] = '1'

app = Celery(
    'practice06',
    broker=RABBITMQ_URL,
    backend=POSTGRES_URL,
)

app.conf.update(
    worker_pool='prefork', # 멀티프로세싱 기반 실행 풀
)

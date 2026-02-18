import os

import billiard
from celery import Celery

from global_config import *

# macOS에서 prefork worker가 정상 동작하도록 기본 방식을 spawn으로 고정
billiard.context._force_start_method('spawn')
os.environ['FORKED_BY_MULTIPROCESSING'] = '1'

app = Celery(
    'practice02',
    broker=RABBITMQ_URL,
    backend=POSTGRES_URL,
)

app.conf.update(
    worker_concurrency=4,  # 동시에 실행할 worker 프로세스 수
    worker_pool='prefork', # 멀티프로세싱 기반 실행 풀
)

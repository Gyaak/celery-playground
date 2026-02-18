import os

import billiard
from celery import Celery
from kombu import Queue

from global_config import RABBITMQ_URL, POSTGRES_URL

# macOS에서 prefork worker가 정상 동작하도록 기본 방식을 spawn으로 고정
billiard.context._force_start_method('spawn')
os.environ['FORKED_BY_MULTIPROCESSING'] = '1'

app = Celery(
    'practice05',
    broker=RABBITMQ_URL,
    backend=POSTGRES_URL,
)

app.conf.update(
    worker_pool='prefork', # 멀티프로세싱 기반 실행 풀
    # 브로커에 생성할 큐 목록 선언
    # 선언하지 않아도 동작하지만, 명시적으로 관리하기 위해 선언
    task_queues=(
        Queue('high'),
        Queue('low'),
    ),
    # 라우팅 규칙을 지정하지 않은 태스크가 보내질 기본 큐
    task_default_queue='low',
)

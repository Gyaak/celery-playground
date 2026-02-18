import os

import billiard
from celery import Celery

from global_config import *

# macOS에서 prefork worker가 정상 동작하도록 기본 방식을 spawn으로 고정
billiard.context._force_start_method('spawn')
os.environ['FORKED_BY_MULTIPROCESSING'] = '1'

# practice00은 태스크 정의와 app 설정을 한 파일에 둔다
# (이후 practice부터는 celery_config.py 로 분리)
app = Celery(
    'practice00',
    broker=RABBITMQ_URL,
    backend=POSTGRES_URL,
    include=['practice00.tasks'],
)


@app.task
def add(x, y):
    return x + y


@app.task
def multiply(x, y):
    return x * y


# 예외를 발생시키는 태스크: AsyncResult 에러 처리 실습용
@app.task
def exception_task():
    raise Exception("This is a test exception")

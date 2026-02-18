import time

from practice05.celery_config import app


# queue='high' 로 라우팅: 데코레이터에 직접 지정
@app.task(queue='high')
def high_priority_task():
    print("[high_priority_task] 실행 중...")
    time.sleep(1)
    return "high done"


# queue 미지정: task_default_queue('low') 로 라우팅
@app.task
def low_priority_task():
    print("[low_priority_task] 실행 중...")
    time.sleep(1)
    return "low done"

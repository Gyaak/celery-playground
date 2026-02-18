"""
큐 라우팅 실습: 태스크별로 큐를 분리하고 worker별로 담당 큐를 지정.

실행:
    터미널 1 — high 큐 전담 worker:
        celery -A practice05.tasks worker --queues=high --loglevel=info --hostname=worker-high@%h

    터미널 2 — low 큐 전담 worker:
        celery -A practice05.tasks worker --queues=low --loglevel=info --hostname=worker-low@%h

    터미널 3 — 태스크 호출:
        python -m practice05.call_tasks
"""
from practice05.tasks import high_priority_task, low_priority_task

if __name__ == "__main__":
    # 데코레이터에 queue='high' 지정 → high 큐로 전송 → worker-high 가 처리
    r1 = high_priority_task.delay()

    # queue 미지정 → task_default_queue('low') 로 전송 → worker-low 가 처리
    r2 = low_priority_task.delay()

    # apply_async의 queue 인자로 호출 시점에 큐를 override
    # low_priority_task 임에도 high 큐로 전송 → worker-high 가 처리
    r3 = low_priority_task.apply_async(queue='high')

    print(r1.get(timeout=10))  # "high done"
    print(r2.get(timeout=10))  # "low done"
    print(r3.get(timeout=10))  # "low done" (high 큐에서 처리됨)

    # 예상 worker 로그:
    # worker-high: [high_priority_task] 실행 중...  ← r1
    #              [low_priority_task] 실행 중...   ← r3 (override)
    # worker-low:  [low_priority_task] 실행 중...   ← r2

"""
retry 동작 실습: 2번 실패 후 3번째 시도에 성공.

실행:
    celery -A practice04.tasks worker --loglevel=info
    python -m practice04.call_tasks
"""
from practice04.tasks import two_fail_task

if __name__ == "__main__":
    r = two_fail_task.delay()
    print(r.get(timeout=30))

    # 예상 worker 로그:
    # [two_fail_task] attempt=0
    # [two_fail_task] 실패! (1/2)
    # [two_fail_task] attempt=1
    # [two_fail_task] 실패! (2/2)
    # [two_fail_task] attempt=2
    # [two_fail_task] 성공! (총 3번 시도)

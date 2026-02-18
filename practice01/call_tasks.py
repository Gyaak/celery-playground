"""
time_limit, soft_time_limit 동작 확인.

실행:
    celery -A practice01.tasks worker --loglevel=info
    python -m practice01.call_tasks
"""
from practice01.tasks import sample_task1, timeouted_task, soft_timeouted_task

if __name__ == "__main__":
    # 제한 없음: 10초 sleep 후 정상 완료
    sample_task1.delay()

    # Hard Timeout: 15초 sleep 시도하지만 10초 후 프로세스 강제 종료
    timeouted_task.delay()

    # Soft Timeout: 15초 sleep 시도 → 10초 후 SoftTimeLimitExceeded 발생
    #               except 블록에서 자원 정리 후 종료
    soft_timeouted_task.delay()

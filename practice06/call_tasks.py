"""
명시적 태스크 이름과 send_task 실습: 태스크를 임포트하지 않고 이름으로 호출.

실행:
    celery -A practice06.tasks worker --loglevel=info
    python -m practice06.call_tasks
"""
from practice06.celery_config import app

if __name__ == "__main__":
    # send_task: tasks.py 를 임포트하지 않고 태스크 이름으로 직접 호출
    # 호출자가 worker 코드에 의존하지 않아도 됨 (마이크로서비스 간 호출에 유용)
    r = app.send_task('email.send_welcome', args=[42])
    print(r.get(timeout=10))  # "email sent to user 42"

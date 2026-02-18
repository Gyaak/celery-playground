from practice06.celery_config import app


# name을 명시하지 않으면 Celery가 모듈 경로로 자동 생성:
#   "practice06.tasks.send_welcome_email"
#
# name을 명시하면 모듈 경로와 무관하게 고정된 이름을 사용:
#   "email.send_welcome"
#
# 명시적 이름을 사용하면:
# - 태스크를 임포트하지 않고 이름만으로 호출 가능 (send_task)
# - 모듈 구조를 리팩터링해도 이름이 바뀌지 않아 안정적
@app.task(name='email.send_welcome')
def send_welcome_email(user_id: int):
    print(f"[send_welcome_email] user_id={user_id} 에게 환영 메일 발송")
    return f"email sent to user {user_id}"

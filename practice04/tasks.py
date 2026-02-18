from practice04.celery_config import app


# bind=True: 태스크 인스턴스(self)를 첫 번째 인자로 받음
# max_retries: 최대 재시도 횟수 (초과 시 MaxRetriesExceededError)
@app.task(bind=True, max_retries=3)
def two_fail_task(self):
    # self.request.retries: 현재 재시도 횟수 (첫 실행=0, 1차 재시도=1, ...)
    attempt = self.request.retries
    print(f"[two_fail_task] attempt={attempt}")

    try:
        if attempt < 2:
            raise RuntimeError(f"Intentional failure on attempt {attempt + 1}")

        print(f"[two_fail_task] 성공! (총 {attempt + 1}번 시도)")
        return f"success on attempt {attempt + 1}"

    except RuntimeError as e:
        print(f"[two_fail_task] 실패! ({attempt + 1}/2)")
        # self.retry(): countdown 초 후 재시도 예약 후 Retry 예외를 반환
        # raise로 던져야 현재 실행이 즉시 중단됨
        raise self.retry(exc=e, countdown=1)

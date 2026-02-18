import time

from celery.exceptions import SoftTimeLimitExceeded

from practice01.celery_config import app


# time_limit/soft_time_limit 미지정: 제한 없이 실행
@app.task
def sample_task1():
    print("sample_task1 started")
    time.sleep(10)
    print("sample_task1 finished")


# time_limit (Hard Timeout): 제한 시간 초과 시 worker 프로세스를 즉시 강제 종료
# 자원 정리 코드가 실행될 기회가 없음
@app.task(time_limit=10)
def timeouted_task():
    print("timeouted_task started")
    time.sleep(15)  # 10초 후 프로세스 강제 종료 → 이 라인 완료 불가
    print("timeouted_task finished")


# soft_time_limit (Soft Timeout): 제한 시간 초과 시 SoftTimeLimitExceeded 예외 발생
# except 블록에서 자원 정리(DB 연결, 파일 닫기 등) 후 종료 가능
# time_limit은 soft_time_limit 초과 후에도 종료되지 않을 경우의 최후 안전장치
@app.task(soft_time_limit=10, time_limit=15)
def soft_timeouted_task():
    try:
        print("soft_timeouted_task started")
        time.sleep(15)  # 10초 후 SoftTimeLimitExceeded 발생
        print("soft_timeouted_task finished")
    except SoftTimeLimitExceeded:
        # soft timeout 발생 시 자원 정리 수행 (hard timeout까지 남은 여유: 15 - 10 = 5초)
        print("SoftTimeOut : 자원 정리 중")
        time.sleep(3)
        print("SoftTimeOut : 자원 정리 완료")

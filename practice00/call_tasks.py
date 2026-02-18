"""
태스크 호출 방법과 AsyncResult 사용법 실습.

실행:
    celery -A practice00.tasks worker --loglevel=info
    python -m practice00.call_tasks
"""
from practice00.tasks import add, multiply, exception_task

if __name__ == "__main__":
    # delay(): 기본 비동기 호출, apply_async(args=...) 의 단축 표현
    r1 = add.delay(4, 5)       # = add.apply_async(args=(4, 5))
    r2 = multiply.delay(3, 7)  # = multiply.apply_async(args=(3, 7))

    # get(): 결과가 나올 때까지 블로킹, timeout 초과 시 TimeoutError
    print(r1.get(timeout=10))  # 9
    print(r2.get(timeout=10))  # 21

    # apply_async(): countdown, eta, expires 등 옵션 지정 가능
    r3 = add.apply_async(args=(10, 20), countdown=1)  # 1초 후 실행
    print(r3.get(timeout=10))  # 30

    # propagate=False: 예외를 호출자에게 전파하지 않고 결과 객체에 담아 반환
    r4 = exception_task.delay()
    r4.get(propagate=False)
    print(r4.ready())      # True  — 완료 여부
    print(r4.successful()) # False — 성공 여부
    print(r4.failed())     # True  — 실패 여부
    print(r4)              # AsyncResult 객체 (task id 포함)
    print(r4.traceback)    # worker에서 발생한 스택 트레이스

    # propagate=True (기본값): worker의 예외가 호출자에게 그대로 전파됨
    r5 = exception_task.delay()
    r5.get(propagate=True)  # 여기서 Exception 발생
    print("never reached")  # 위에서 예외가 발생하므로 실행되지 않음

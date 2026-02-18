"""
chain을 이용한 순차 파이프라인 실습.

실행:
    celery -A practice02.tasks worker --loglevel=info
    python -m practice02.call_tasks

실행 흐름:
    sum(1.0, 2.0) → 3.0
                     ↓
    multiply(3.0, 3.0) → 9.0
                          ↓
    divide(9.0, 7.0) → 1.285...
                         ↓
    subtract(1.285..., 2.0) → -0.714...
"""
import uuid

from celery import chain
from celery.result import AsyncResult

from practice02.tasks import sum_task, multiply_task, divide_task, subtract_task

if __name__ == "__main__":
    # 각 단계의 결과를 개별 조회하기 위해 task_id를 미리 지정
    id1 = str(uuid.uuid4())
    id2 = str(uuid.uuid4())
    id3 = str(uuid.uuid4())
    id4 = str(uuid.uuid4())

    # .s(): 태스크 시그니처 생성 (즉시 실행하지 않음)
    # chain에서 두 번째 이후 태스크는 앞 결과를 첫 인자로 받으므로 나머지 인자만 지정
    workflow = chain(
        sum_task.s(1.0, 2.0).set(task_id=id1),   # sum(1.0, 2.0)       → 3.0
        multiply_task.s(3.0).set(task_id=id2),    # multiply(3.0, 3.0)  → 9.0
        divide_task.s(7.0).set(task_id=id3),      # divide(9.0, 7.0)    → 1.285...
        subtract_task.s(2.0).set(task_id=id4),    # subtract(1.285, 2.0)→ -0.714...
    )
    workflow.apply_async()

    # 각 단계 결과를 task_id로 개별 조회
    print(f"result of {id1}: {AsyncResult(id1).get()}")  # 3.0
    print(f"result of {id2}: {AsyncResult(id2).get()}")  # 9.0
    print(f"result of {id3}: {AsyncResult(id3).get()}")  # 1.285...
    print(f"result of {id4}: {AsyncResult(id4).get()}")  # -0.714...

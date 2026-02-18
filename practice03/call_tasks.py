"""
chord(group + 콜백)를 이용한 병렬 실행 및 결과 집계 실습.

실행:
    celery -A practice03.tasks worker --loglevel=info
    python -m practice03.call_tasks

실행 흐름:
    short_task ─┐
    long_task   ├─ (모두 완료 대기) ─→ merge_task([result1, ..., result5])
    short_task  │
    short_task  │
    short_task ─┘
"""
import uuid

from celery import chord, group
from celery.result import AsyncResult

from practice03.tasks import short_task, long_task, merge_task

if __name__ == "__main__":
    id1 = str(uuid.uuid4())
    id2 = str(uuid.uuid4())
    id3 = str(uuid.uuid4())
    id4 = str(uuid.uuid4())
    id5 = str(uuid.uuid4())
    id6 = str(uuid.uuid4())

    # chord: group의 모든 태스크가 완료된 후 콜백(merge_task)을 실행
    # 콜백은 각 태스크의 반환값을 순서대로 담은 리스트를 첫 번째 인자로 받음
    chord(
        group(
            short_task.s().set(task_id=id1),
            long_task.s().set(task_id=id2),   # 가장 느린 태스크 — 이것이 완료돼야 콜백 실행
            short_task.s().set(task_id=id3),
            short_task.s().set(task_id=id4),
            short_task.s().set(task_id=id5),
        ),
    )(merge_task.s().set(task_id=id6))

    # 콜백(merge_task)의 결과를 기다림
    print(f"result of {id6}: {AsyncResult(id6).get()}")

    # 예상 worker 로그 (concurrency=4 기준):
    # short_task x4 가 병렬 실행 → 약 1초 후 완료
    # long_task 는 10초 후 완료 → 이 시점에 merge_task 트리거
    # short_task (5번째) 는 빈 worker 슬롯이 생기면 실행

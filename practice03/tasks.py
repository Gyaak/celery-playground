import time

from practice03.celery_config import app

# chord 실습용 태스크
# group으로 병렬 실행하고, 모두 완료되면 merge_task(콜백)가 결과 리스트를 받음

@app.task
def short_task():
    print("short_task started")
    time.sleep(1)
    print("short_task finished")
    return "short_task finished"


@app.task
def long_task():
    print("long_task started")
    time.sleep(10)
    print("long_task finished")
    return "long_task finished"


# chord 콜백 태스크: group의 모든 태스크 결과가 리스트로 전달됨
@app.task
def merge_task(results):
    final_result = "\nMerge task result:\n"
    for i, result in enumerate(results):
        final_result += f"{i+1}th task result: {result}\n"
    return final_result

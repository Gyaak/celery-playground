from practice02.celery_config import app

# chain 실습용 산술 태스크
# chain에서 앞 태스크의 반환값이 다음 태스크의 첫 번째 인자로 자동 전달됨

@app.task
def sum_task(x: float, y: float):
    return x + y


@app.task
def multiply_task(x: float, y: float):
    return x * y


@app.task
def divide_task(x: float, y: float):
    return x / y


@app.task
def subtract_task(x: float, y: float):
    return x - y

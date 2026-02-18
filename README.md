# Celery Playground

Celery의 다양한 기능을 단계별로 학습하는 실습 프로젝트입니다.

## 인프라

```bash
docker-compose up -d
```

| 서비스 | 포트 | 용도 |
|--------|------|------|
| RabbitMQ | 5672 / 15672 (UI) | 메시지 브로커 |
| PostgreSQL | 5432 | 결과 백엔드 |
| Redis | 6379 / 8001 (UI) | 결과 백엔드 (practice03) |

**접속 정보 (`global_config.py`)**
```python
REDIS_URL    = "redis://localhost:6379"
RABBITMQ_URL = "amqp://localhost:5672"
POSTGRES_URL = "db+postgresql://postgres:postgres@localhost:5432/celery_jobs"
```

---

## practice00 — 기본 태스크 호출

**핵심 개념**
- `task.delay(*args)` — 기본 비동기 호출
- `task.apply_async(args=..., countdown=N)` — 옵션 지정 호출
- `AsyncResult` — `get()`, `ready()`, `successful()`, `failed()`, `traceback`
- `get(propagate=False)` — 예외를 던지지 않고 결과 반환

```bash
celery -A practice00.tasks worker --loglevel=info
python -m practice00.call_tasks
```

---

## practice01 — 태스크 타임아웃

**핵심 개념**

| | `time_limit` (Hard) | `soft_time_limit` (Soft) |
|--|---------------------|--------------------------|
| 동작 | 프로세스 즉시 강제 종료 | `SoftTimeLimitExceeded` 예외 발생 |
| 자원 정리 | 불가 | `except` 블록에서 처리 가능 |
| 용도 | 최후 안전장치 | Graceful shutdown |

두 옵션을 함께 쓰는 것이 일반적: soft로 정리 기회를 주고, hard로 최종 시간을 보장.

```bash
celery -A practice01.tasks worker --loglevel=info
python -m practice01.call_tasks
```

---

## practice02 — Chain (순차 파이프라인)

**핵심 개념**
- `chain`: 앞 태스크의 반환값이 다음 태스크의 첫 번째 인자로 자동 전달
- `.s()` Signature: 즉시 실행하지 않고 워크플로우 조합에 사용
- `.set(task_id=...)`: 중간 결과를 개별 조회하기 위한 custom ID 지정

```
sum(1, 2) → 3.0 → multiply(3.0, 3) → 9.0 → divide(9.0, 7) → 1.285 → subtract(1.285, 2) → -0.714
```

```bash
celery -A practice02.tasks worker --loglevel=info
python -m practice02.call_tasks
```

---

## practice03 — Chord (병렬 실행 + 콜백)

**핵심 개념**
- `group`: 여러 태스크를 병렬 실행
- `chord`: group + 콜백 — 모든 태스크 완료 후 결과 리스트를 콜백으로 전달

**백엔드별 완료 감지 방식**

| | PostgreSQL | Redis |
|--|------------|-------|
| 감지 방식 | `chord_unlock` 폴링 (1초마다) | atomic `INCR` 카운터 |
| 완료 감지 | 최대 1초 지연 | 즉시 |

> practice03은 즉시 감지를 위해 Redis를 백엔드로 사용합니다.

```bash
celery -A practice03.tasks worker --loglevel=info
python -m practice03.call_tasks
```

---

## practice04 — Retry (재시도)

**핵심 개념**
- `bind=True`: `self`(태스크 인스턴스)를 첫 번째 인자로 받음
- `self.request.retries`: 현재 재시도 횟수 (0부터 시작)
- `raise self.retry(exc=e, countdown=N)`: N초 후 재시도 예약 후 현재 실행 즉시 중단
- 실무 패턴: `try/except`로 실제 예외를 잡아 `self.retry()`로 전달

```python
@app.task(bind=True, max_retries=3)
def task(self):
    try:
        ...
    except SomeError as e:
        raise self.retry(exc=e, countdown=1)
```

```bash
celery -A practice04.tasks worker --loglevel=info
python -m practice04.call_tasks
```

---

## practice05 — 큐 라우팅

**핵심 개념**
- `task_queues`: 브로커에 생성할 큐 목록 선언
- `task_default_queue`: 라우팅 규칙 없는 태스크의 기본 큐
- `@app.task(queue='...')`: 데코레이터로 태스크를 특정 큐에 고정
- `.apply_async(queue='...')`: 호출 시점에 큐를 override
- `--queues=<name>`: worker가 소비할 큐 지정

**큐를 분리하는 이유**: 태스크 종류별로 worker 자원을 격리하여, 느린 태스크가 빠른 태스크를 블로킹하지 않도록 하고 중요도에 따라 자원을 배분하기 위함.

```bash
# 큐별로 worker를 따로 실행해야 라우팅 효과를 확인할 수 있음
celery -A practice05.tasks worker --queues=high --loglevel=info --hostname=worker-high@%h
celery -A practice05.tasks worker --queues=low  --loglevel=info --hostname=worker-low@%h
python -m practice05.call_tasks
```

---

## practice06 — 명시적 태스크 이름 & send_task

**핵심 개념**
- `@app.task(name='...')`: 태스크 이름을 명시적으로 지정. 미지정 시 `모듈경로.함수명`으로 자동 생성
- `app.send_task('name', args=[...])`: 태스크 함수를 임포트하지 않고 이름만으로 호출
- 명시적 이름을 쓰면 모듈 구조를 리팩터링해도 이름이 바뀌지 않아 안정적

```python
# tasks.py (worker 쪽)
@app.task(name='email.send_welcome')
def send_welcome_email(user_id: int): ...

# call_tasks.py (호출자 쪽) — tasks.py 임포트 없음
app.send_task('email.send_welcome', args=[42])
```

```bash
celery -A practice06.tasks worker --loglevel=info
python -m practice06.call_tasks
```

---

## 프로젝트 설정

**요구사항**: Python 3.13+, [uv](https://docs.astral.sh/uv/)

```bash
uv sync
```

**의존성**
- `celery>=5.5`
- `psycopg2-binary>=2.9.11`
- `redis>=7.2.0`
- `sqlalchemy>=2.0.46`

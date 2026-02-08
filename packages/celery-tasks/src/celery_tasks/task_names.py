"""Celery Task 이름 상수 정의."""

from enum import Enum


class TaskNames(str, Enum):
    """Celery Task 이름을 관리하는 Enum."""

    PROCESS_JOB = "tasks.process_job"

    def __str__(self) -> str:
        """문자열 변환 시 value 반환."""
        return self.value

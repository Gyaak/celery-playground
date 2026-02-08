FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy workspace files
COPY pyproject.toml ./
COPY packages/ ./packages/
COPY celery-worker/ ./celery-worker/

# Install dependencies
RUN uv pip install --system -e ./packages/celery-postgres -e ./packages/celery-redis -e ./packages/celery-tasks -e ./celery-worker

# Run Celery worker
CMD ["python", "-m", "celery_worker"]

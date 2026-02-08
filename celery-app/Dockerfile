FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy workspace files
COPY pyproject.toml ./
COPY packages/ ./packages/
COPY celery-app/ ./celery-app/

# Install dependencies
RUN uv pip install --system -e ./packages/celery-postgres -e ./packages/celery-redis -e ./packages/celery-tasks -e ./celery-app

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["python", "-m", "celery_app"]

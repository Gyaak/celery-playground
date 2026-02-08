import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from celery_app.routers import job_router
from celery_postgres import Base, sync_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리."""
    # Startup: 데이터베이스 테이블 생성
    Base.metadata.create_all(bind=sync_engine)
    print("Database tables created successfully")
    yield
    # Shutdown: 필요한 정리 작업이 있으면 여기에 추가


# FastAPI 앱 생성
app = FastAPI(
    title="Celery Job Manager API",
    description="API for managing Celery jobs with 3-step processing",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(job_router)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Celery Job Manager API is running"}


if __name__ == "__main__":
    uvicorn.run(
        "celery_app.__main__:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

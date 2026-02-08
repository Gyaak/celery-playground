from dotenv import find_dotenv
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    POSTGRES_HOST: str ="localhost"
    POSTGRES_PORT: int = 5678
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"

    class Config:
        env_file = find_dotenv()
        env_file_encoding = "utf-8"
        extra = "ignore"
    
    @property
    def sync_database_url(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def async_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def celery_backend_url(self) -> str:
        """Celery result backend URL (db+postgresql:// 형식)"""
        return f"db+postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

db_settings = DBSettings()

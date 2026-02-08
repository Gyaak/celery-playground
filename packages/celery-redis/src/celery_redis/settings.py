from pydantic_settings import BaseSettings
from dotenv import find_dotenv


class RedisSettings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    class Config:
        env_file = find_dotenv()
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def redis_url(self) -> str:
        """Redis connection URL for Celery broker."""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


redis_settings = RedisSettings()

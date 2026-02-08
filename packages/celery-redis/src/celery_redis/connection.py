import redis
from .settings import redis_settings


def get_redis_client() -> redis.Redis:
    """Get Redis client instance."""
    return redis.Redis(
        host=redis_settings.REDIS_HOST,
        port=redis_settings.REDIS_PORT,
        db=redis_settings.REDIS_DB,
        password=redis_settings.REDIS_PASSWORD,
        decode_responses=True,
    )


def get_redis_connection_pool() -> redis.ConnectionPool:
    """Get Redis connection pool."""
    return redis.ConnectionPool(
        host=redis_settings.REDIS_HOST,
        port=redis_settings.REDIS_PORT,
        db=redis_settings.REDIS_DB,
        password=redis_settings.REDIS_PASSWORD,
        decode_responses=True,
    )

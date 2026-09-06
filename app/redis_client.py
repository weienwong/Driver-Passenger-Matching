"""Shared Redis client factory."""

from functools import lru_cache

from redis import Redis

from app.config import get_settings


@lru_cache
def get_redis_client() -> Redis:
    """Create a shared Redis client using the configured connection URL."""

    return Redis.from_url(get_settings().redis_url, decode_responses=True)

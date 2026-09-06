"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated runtime settings for the API and background workers."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    redis_url: str
    lta_api_url: str = "https://api.data.gov.sg/v1/transport/taxi-availability"
    lta_request_timeout_seconds: float = Field(default=10, gt=0)
    polling_interval_seconds: int = Field(default=600, ge=60)
    redis_snapshot_ttl_seconds: int = Field(default=600, ge=1)
    matching_search_radius_km: float = Field(default=5, gt=0)
    matching_candidate_count: int = Field(default=50, ge=1, le=500)
    matching_reservation_ttl_seconds: int = Field(default=60, ge=1)
    matching_max_retries: int = Field(default=3, ge=1)
    matching_retry_seconds: float = Field(default=5, ge=0)


@lru_cache
def get_settings() -> Settings:
    """Return the cached, validated application settings."""

    return Settings()

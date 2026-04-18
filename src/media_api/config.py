from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    discord_api_secret: str
    log_level: str = "INFO"
    metadata_cache_ttl: int = 3600
    stream_url_cache_ttl: int = 300
    ydl_format: str = "bestaudio/best"
    max_search_results: int = 10


@lru_cache
def get_settings() -> Settings:
    return Settings()

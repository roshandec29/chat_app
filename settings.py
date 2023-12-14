from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGODB_URI: str
    REDIS_URL: str
    REDIS_PORT: str
    REDIS_HOST: str
    IMAGE_KIT_PUBLIC_KEY: str
    IMAGE_KIT_PRIVATE_KEY: str
    IMAGE_KIT_URL: str
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()
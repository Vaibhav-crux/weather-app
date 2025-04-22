from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    api_key: str
    environment: str = "development"
    port: int = 8001
    WEATHER_API_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()
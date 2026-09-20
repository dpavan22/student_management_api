from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Student Management API"
    DEBUG: bool = True
    
    DATABASE_URL : str = "sqlite:///./student_app.db"
    
    
    SECRET_KEY: str = 'dev-secret-key-12345'
    ALGORITM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = Settings()
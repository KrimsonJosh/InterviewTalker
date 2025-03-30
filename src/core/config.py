from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str
    DEEPGRAM_API_KEY: str
    
    # Application Settings
    APP_NAME: str = "InterviewTalker"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings() 
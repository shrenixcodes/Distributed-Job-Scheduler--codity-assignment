
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./scheduler.db"  # Use SQLite for local dev
    SECRET_KEY: str = "your-secret-key-keep-it-safe-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

settings = Settings()

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Tạo engine cho PostgreSQL
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Tạo session factory
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
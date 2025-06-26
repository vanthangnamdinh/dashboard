from dotenv import load_dotenv
load_dotenv()

import os
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    JWT_ALGORITHM: str = "RSA256"
    SENTRY_SDN: str = ""

    # JWT RS256 config
    JWT_ISSUER: str = os.getenv("JWT_ISSUER", "your_issuer")
    JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "your_audience")
    JWT_PUBLIC_KEY_URL: str = os.getenv("JWT_PUBLIC_KEY_URL", "https://your-domain/.well-known/jwks.json")

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "dashboard")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_URL: str =os.getenv("POSTGRES_PASSWORD", f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}") 

class TestConfig(Config):
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "dashboard")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_URL: str =os.getenv("POSTGRES_PASSWORD", f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}") 

class LocalConfig(Config):
    ...

class ProductionConfig(Config):
    DEBUG: bool = False

def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "test": TestConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]

config: Config = get_config()
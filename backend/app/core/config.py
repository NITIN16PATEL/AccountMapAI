from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "AccountMap AI"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "dev-secret-key-change-me"
    database_url: str = "sqlite:///./accountmap.db"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    rate_limit_per_minute: int = 120
    allowed_hosts: list[str] = ["*"]
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    demo_mode: bool = True
    ai_provider: str = "local"
    ai_api_key: str = ""
    gmail_client_id: str = ""
    gmail_client_secret: str = ""
    gmail_redirect_uri: str = "http://localhost:8000/api/auth/google/callback"
    microsoft_client_id: str = ""
    microsoft_client_secret: str = ""
    microsoft_redirect_uri: str = "http://localhost:8000/api/auth/microsoft/callback"
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "accountmap"
    mysql_password: str = "password"
    mysql_database: str = "accountmap"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

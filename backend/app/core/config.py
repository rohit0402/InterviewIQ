from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # ==========================
    # Project
    # ==========================
    project_name: str = "InterviewIQ API"
    version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"

    # ==========================
    # Environment
    # ==========================
    environment: str = "development"
    debug: bool = True

    # ==========================
    # Database
    # ==========================
    database_url: str

    # ==========================
    # JWT Authentication
    # ==========================
    secret_key: str
    algorithm: str = "HS256"

    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # ==========================
    # CORS
    # ==========================
    backend_cors_origins: str = "http://localhost:5173"

    # ==========================
    # Logging
    # ==========================
    log_level: str = "INFO"

    # ==========================
    # Pydantic Settings
    # ==========================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore unknown variables in .env
    )


settings = Settings()
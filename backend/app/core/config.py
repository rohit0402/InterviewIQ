from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    AI_API_KEY: str
    AI_MODEL: str    
    AI_PROVIDER: str

    project_name: str = "InterviewIQ API"
    version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"

    environment: str = "development"
    debug: bool = True

    database_url: str

    secret_key: str
    algorithm: str = "HS256"

    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    backend_cors_origins: str = "http://localhost:5173"

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore", 
    )


settings = Settings()
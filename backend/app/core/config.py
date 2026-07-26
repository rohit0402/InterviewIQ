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

    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_from_email: str

    frontend_url: str


    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    @property
    def redis_url(self)->str:
        if self.REDIS_PASSWORD:
            return (f"redis://:{self.REDIS_PASSWORD}@" f"{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}")
        return (f"redis://{self.REDIS_HOST}:" f"{self.REDIS_PORT}/{self.REDIS_DB}")

settings = Settings()
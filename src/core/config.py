"""Settings module for the FastAPI application."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "Hub do Saber"
    PROJECT_DESCRIPTION: str

    DEBUG: bool = True

    # API
    API_VERSION: str = "v1"
    API_V1_STR: str = "/api/v1"

    FRONTEND_URL: str

    # Database
    DATABASE_DEV_URL: str = ""
    DATABASE_PROD_URL: str = ""
    DATABASE_ECHO: bool = True
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    DATABASE_POOL_PRE_PING: bool = True
    DATABASE_RECYCLE: int = 3600

    # Security
    SECRET_KEY: str = "Otlevire"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 604800  # 7 days

    # Root Admin Data
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    ADMIN_FULL_NAME: str
    ADMIN_PHONE: str
    ADMIN_USERNAME: str

    # OPENAI CONFIGURATION
    OPENAI_API_KEY: str
    OPENAI_DEFAULT_MODEL: str

    # MESSAGE PROCESSING
    VERBOSE: bool = True
    MESSAGE_RESPONSE_TEMPERATURE: float
    MESSAGES_MAX_TOKENS: int
    MESSAGES_MAX_NUMBER_IN_HISTORIC: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def database_url(self) -> str:
        """Return the database URL based on the DEBUG flag."""
        if self.DEBUG:
            return self.DATABASE_DEV_URL
        return self.DATABASE_PROD_URL


settings = Settings()

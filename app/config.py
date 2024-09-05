from typing import List, Optional

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):

    # db settings
    POSTGRES_SERVER: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "url_shortener"
    POSTGRES_PORT: int = "5432"
    DATABASE_URL: Optional[PostgresDsn] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DATABASE_URL = PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=f"{self.POSTGRES_DB}",
        )

    # API settings
    API_PREFIX: str = ""
    ALLOWED_HOSTS: List[str] = ["*"]

    # URL settings
    BASE_URL: str = "http://localhost:8000"

    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
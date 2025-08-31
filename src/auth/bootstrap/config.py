from dataclasses import dataclass
from datetime import timedelta
from functools import lru_cache
from os import environ
from pathlib import Path
from typing import Self

from dotenv import load_dotenv

from auth.infrastructure.outbox.config import RabbitConfig
from auth.infrastructure.persistence.sqlalchemy.config import PostgresConfig

load_dotenv()


@dataclass(slots=True, frozen=True)
class AppConfig:
    """Класс конфигурации приложения."""

    server_host: str
    server_port: int
    openapi_url: str
    client_id: str
    client_secret: str
    cors_origins: list[str]
    debug: bool

    @classmethod
    def from_env(cls) -> Self:
        """Возвращает настройки приложения."""
        server_host = environ.get("SERVER_HOST", default="127.0.0.1")
        server_port = int(environ.get("SERVER_PORT", default="8000"))
        openapi_url = environ.get("OPENAPI_URL", default="/swagger/docs/v1.0/core")
        client_id = environ.get("CLIENT_ID", default="fastapi")
        client_secret = environ.get("CLIENT_SECRET", default="fastapi_secret")
        cors_origins = environ.get("CORS_ORIGINS", default="*").split(",")
        str_debug = environ.get("DEBUG", default="False")
        debug = str_debug.lower() == "true"

        return cls(
            server_host=server_host,
            server_port=server_port,
            openapi_url=openapi_url,
            client_id=client_id,
            client_secret=client_secret,
            cors_origins=cors_origins,
            debug=debug,
        )


@dataclass(slots=True, frozen=True)
class AuthConfig:
    algorithm: str
    access_token_expires_minutes: timedelta
    refresh_token_expires_minutes: timedelta
    private_key_path: Path
    public_key_path: Path

    @classmethod
    def from_env(cls) -> Self:
        algorithm = environ.get("ALGORITHM", default="HS256")
        access_token_expires_minutes = timedelta(
            minutes=int(environ.get("ACCESS_TOKEN_EXPIRES_MINUTES", default="15"))
        )
        refresh_token_expires_minutes = timedelta(
            minutes=int(environ.get("REFRESH_TOKEN_EXPIRES_MINUTES", default="60"))
        )

        private_key_env = environ.get("PRIVATE_KEY_PATH", "certs/private.pem")
        public_key_env = environ.get("PUBLIC_KEY_PATH", "certs/public.pem")
        private_key_path = Path(private_key_env)
        public_key_path = Path(public_key_env)

        if not private_key_path.is_absolute():
            private_key_path = Path.cwd() / private_key_path

        if not public_key_path.is_absolute():
            public_key_path = Path.cwd() / public_key_path

        return cls(
            algorithm=algorithm,
            access_token_expires_minutes=access_token_expires_minutes,
            refresh_token_expires_minutes=refresh_token_expires_minutes,
            private_key_path=private_key_path,
            public_key_path=public_key_path,
        )


@dataclass(frozen=True)
class Config:
    postgres_config: PostgresConfig
    rabbit_config: RabbitConfig
    auth_config: AuthConfig
    app_config: AppConfig


@lru_cache
def get_config() -> Config:
    return Config(
        postgres_config=PostgresConfig.from_env(),
        rabbit_config=RabbitConfig.from_env(),
        auth_config=AuthConfig.from_env(),
        app_config=AppConfig.from_env(),
    )

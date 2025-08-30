from dataclasses import dataclass
from os import environ
from typing import Self

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class PostgresConfig:
    """Класс конфигурации для PostgreSQL."""

    host: str
    port: int
    user: str
    password: str
    db: str

    uri: str

    @classmethod
    def from_env(cls) -> Self:
        """Возвращает настройки PostgreSQL."""
        host = environ.get("POSTGRES_HOST", "localhost")
        port = int(environ.get("POSTGRES_PORT", "5432"))
        user = environ.get("POSTGRES_USER", "postgres")
        password = environ.get("POSTGRES_PASSWORD", "postgres")
        db = environ.get("POSTGRES_DATABASE", "postgres")

        uri = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

        return cls(host=host, port=port, user=user, password=password, db=db, uri=uri)

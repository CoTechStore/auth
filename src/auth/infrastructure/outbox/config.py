from dataclasses import dataclass
from os import environ
from typing import Self

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True, frozen=True)
class RabbitConfig:
    user: str
    password: str
    host: str
    port: int

    uri: str

    @classmethod
    def from_env(cls) -> Self:
        """Возвращает настройки приложения."""
        user = environ.get("RABBIT_USER", "guest")
        password = environ.get("RABBIT_PASSWORD", "guest")
        host = environ.get("RABBIT_HOST", "localhost")
        port = int(environ.get("RABBIT_PORT", "5672"))

        uri = f"amqp://{user}:{password}@{host}:{port}"

        return cls(user=user, password=password, host=host, port=port, uri=uri)

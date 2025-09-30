from dataclasses import dataclass
from enum import StrEnum
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
    timeout: int
    interval: float

    @classmethod
    def from_env(cls) -> Self:
        """Возвращает настройки приложения."""
        user = environ.get("RABBIT_USER", "guest")
        password = environ.get("RABBIT_PASSWORD", "guest")
        host = environ.get("RABBIT_HOST", "localhost")
        port = int(environ.get("RABBIT_PORT", "5672"))
        timeout = int(environ.get("RABBIT_TIMEOUT", "5"))
        interval = float(environ.get("TASKIQ_INTERVAL", "5"))

        return cls(
            user=user,
            password=password,
            host=host,
            port=port,
            timeout=timeout,
            interval=interval,
        )

    @property
    def uri(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}"


class ExchangeName(StrEnum):
    AUTH = "auth"


class QueueName(StrEnum):
    AUTH = "auth-queue"


class RoutingKeyName(StrEnum):
    USER = "User*"

from dataclasses import dataclass


@dataclass(frozen=True)
class BaseRequest[TResponse]:
    """Общий маркер запроса."""


@dataclass(frozen=True)
class Command[TResponse](BaseRequest[TResponse]):
    """Маркер команды."""


@dataclass(frozen=True)
class Query[TResponse](BaseRequest[TResponse]):
    """Маркер запроса."""

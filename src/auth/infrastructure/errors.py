from dataclasses import dataclass


@dataclass(frozen=True)
class InfrastructureError(Exception):
    """Общей класс для инфраструктурных ошибок."""

    message: str


@dataclass(frozen=True)
class HandlerNotFoundError(InfrastructureError):
    """Обработчик не найден."""

from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValueObject(ABC):
    """Базовый класс для объектов значений."""

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None: ...

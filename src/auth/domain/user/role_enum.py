from collections.abc import Iterable
from enum import Enum
from typing import Self


class BaseRoleEnum(Enum):
    _level: int

    def __new__(cls, role: str, level: int) -> Self:
        obj = object.__new__(cls)
        obj._value_ = role
        obj._level = level  # Добавляем уровень как атрибут
        return obj

    @property
    def level(self) -> int:
        return self._level

    @classmethod
    def list(cls) -> Iterable[str]:
        return tuple(c.name for c in cls)


class AdminRoleEnum(BaseRoleEnum):
    admin = "admin", 100
    technic = "technic", 80


class StaffRoleEnum(BaseRoleEnum):
    engineer = "engineer", 40
    driver = "driver", 10


class RoleEnum(BaseRoleEnum):
    admin = "admin", 100
    technic = "technic", 80
    engineer = "engineer", 40
    driver = "driver", 10

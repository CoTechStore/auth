from enum import StrEnum
from collections.abc import Iterable


class UserType(StrEnum):
    DEFAULT_USER = "default-user"
    SUPER_USER = "super-user"

    @classmethod
    def list(cls) -> Iterable[str]:
        return tuple(c for c in cls)

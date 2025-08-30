from dataclasses import dataclass, field
from enum import Enum, auto

from auth.application.common.const import errors as text


class AppErrorType(Enum):
    NOT_FOUND = auto()
    VALIDATION = auto()
    APPLICATION = auto()
    UNAUTHORIZED = auto()
    UNAUTHENTICATED = auto()
    FORBIDDEN = auto()
    CONFLICT = auto()


@dataclass(frozen=True)
class ApplicationError(Exception):
    message: str = field(default=text.APPLICATION_FORBIDDEN)
    type: AppErrorType = field(default=AppErrorType.APPLICATION)

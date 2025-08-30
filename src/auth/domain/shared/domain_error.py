from dataclasses import dataclass, field
from enum import Enum, auto

from auth.domain.shared.const import errors as text


class DomainErrorType(Enum):
    VALIDATION = auto()
    DOMAIN = auto()
    FORBIDDEN = auto()


@dataclass(frozen=True)
class DomainError(Exception):
    message: str = field(default=text.DOMAIN_FORBIDDEN)
    type: DomainErrorType = field(default=DomainErrorType.DOMAIN)

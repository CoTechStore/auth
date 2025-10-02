import re
from dataclasses import dataclass

from auth.domain.shared.domain_error import DomainError, DomainErrorType
from auth.domain.shared.value_object import ValueObject
from auth.domain.user.const import errors as text
from auth.domain.user.const import login


@dataclass(frozen=True, slots=True)
class Username(ValueObject):
    """Объект значения Логина."""

    value: str

    def _validate(self) -> None:
        """Валидация роли."""
        if len(self.value) == 0:
            raise DomainError(type=DomainErrorType.VALIDATION, message=text.EMPTY_LOGIN)
        if len(self.value) < login.MIN_LENGTH:
            raise DomainError(
                type=DomainErrorType.VALIDATION, message=text.TOO_SHORT_LOGIN
            )
        if len(self.value) > login.MAX_LENGTH:
            raise DomainError(
                type=DomainErrorType.VALIDATION, message=text.TOO_LONG_LOGIN
            )
        if not re.match(login.PATTERN, self.value):
            raise DomainError(
                type=DomainErrorType.VALIDATION, message=text.WRONG_LOGIN_FORMAT
            )

import re
from dataclasses import dataclass

from auth.domain.shared.domain_error import DomainError, DomainErrorType
from auth.domain.shared.value_object import ValueObject
from auth.domain.user.const import errors as text
from auth.domain.user.const import password


@dataclass(frozen=True)
class Password(ValueObject):
    """Объект значения Пароля."""

    value: str

    def _validate(self) -> None:
        """Валидация пароля."""
        if len(self.value) == 0:
            raise DomainError(
                type=DomainErrorType.VALIDATION, message=text.EMPTY_PASSWORD
            )
        if len(self.value) < password.MIN_LENGTH:
            raise DomainError(
                type=DomainErrorType.VALIDATION, message=text.TOO_SHORT_PASSWORD
            )
        if len(self.value) > password.MAX_LENGTH:
            raise DomainError(
                type=DomainErrorType.VALIDATION, message=text.TOO_LONG_PASSWORD
            )
        if not re.match(password.PATTERN, self.value):
            raise DomainError(
                type=DomainErrorType.VALIDATION, message=text.WRONG_PASSWORD_FORMAT
            )

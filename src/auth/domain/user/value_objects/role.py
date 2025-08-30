from dataclasses import dataclass

from auth.domain.shared.domain_error import DomainError, DomainErrorType
from auth.domain.shared.value_object import ValueObject
from auth.domain.user.const.errors import EXTENDED_FORBIDDEN
from auth.domain.user.role_enum import StaffRoleEnum


@dataclass(frozen=True)
class Role(ValueObject):
    """Объект значения Роли."""

    name: str
    extended: bool

    def validate(self) -> None:
        if self.name == StaffRoleEnum.driver.name and self.extended:
            raise DomainError(type=DomainErrorType.FORBIDDEN, message=EXTENDED_FORBIDDEN)

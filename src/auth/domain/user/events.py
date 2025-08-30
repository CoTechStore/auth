from dataclasses import dataclass

from auth.domain.shared.domain_event import DomainEvent
from auth.domain.user.value_objects import UserId


@dataclass(frozen=True, slots=True)
class PasswordChanged(DomainEvent):
    user_id: UserId
    hash_password: bytes


@dataclass(frozen=True, slots=True)
class RoleChanged(DomainEvent):
    user_id: UserId
    role_name: str
    role_extended: bool


@dataclass(frozen=True, slots=True)
class UserHiddenOrRevealed(DomainEvent):
    user_id: UserId
    hidden: bool

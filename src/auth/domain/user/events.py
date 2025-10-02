from dataclasses import dataclass

from auth.domain.shared.domain_event import DomainEvent
from auth.domain.user.value_objects import UserId


@dataclass(frozen=True, slots=True)
class UserCreated(DomainEvent):
    user_id: UserId


@dataclass(frozen=True, slots=True)
class UserPasswordChanged(DomainEvent):
    user_id: UserId
    hash_password: bytes


@dataclass(frozen=True, slots=True)
class UserRoleChanged(DomainEvent):
    user_id: UserId
    name: str
    extended: bool


@dataclass(frozen=True, slots=True)
class UserHiddenOrRevealed(DomainEvent):
    user_id: UserId
    hidden: bool

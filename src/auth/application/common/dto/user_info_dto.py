from dataclasses import dataclass

from auth.domain.user.value_objects import UserId


@dataclass(frozen=True, slots=True)
class UserInfoDto:
    id: UserId
    login: str
    role: str
    extended: bool
    hidden: bool
    organization_name: str | None

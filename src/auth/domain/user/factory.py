from abc import ABC, abstractmethod

from auth.domain.user.user import User
from auth.domain.user.value_objects import Login, Role, UserId


class UserFactory(ABC):
    @abstractmethod
    async def create_user(
        self,
        user_id: UserId,
        login: Login,
        hash_password: bytes,
        hidden: bool,
        role: Role,
        organization_name: str | None,
    ) -> User: ...

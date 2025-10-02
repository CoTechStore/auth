from abc import ABC, abstractmethod
from typing import Unpack

from auth.domain.user.specifications import UserSpecifications
from auth.domain.user.user import User
from auth.domain.user.value_objects import UserId


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None: ...

    @abstractmethod
    async def find(self, **specifications: Unpack[UserSpecifications]) -> User | None: ...

    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> User | None: ...

    @abstractmethod
    async def with_username(self, username: str) -> User | None: ...

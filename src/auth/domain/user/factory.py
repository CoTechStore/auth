from abc import ABC, abstractmethod

from auth.domain.user.user import User
from auth.domain.user.value_objects import Username, Password


class UserFactory(ABC):
    @abstractmethod
    async def create_user(self, username: Username, password: Password) -> User: ...

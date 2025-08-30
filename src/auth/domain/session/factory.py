from abc import ABC, abstractmethod
from datetime import datetime

from auth.domain.session.session import Session
from auth.domain.user.value_objects import UserId


class SessionFactory(ABC):
    @abstractmethod
    async def authenticate_user(
        self, user_id: UserId, iat: datetime, expires: datetime
    ) -> Session: ...

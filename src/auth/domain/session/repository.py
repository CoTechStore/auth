from abc import ABC, abstractmethod

from auth.domain.session.session import Session
from auth.domain.session.session_id import SessionId
from auth.domain.user.value_objects import UserId


class SessionRepository(ABC):
    @abstractmethod
    def add(self, session: Session) -> None: ...

    @abstractmethod
    async def delete(self, session: Session) -> None: ...

    @abstractmethod
    async def with_session_id(self, session_id: SessionId) -> Session | None: ...

    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> list[Session]: ...

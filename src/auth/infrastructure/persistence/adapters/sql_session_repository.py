from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.domain.session.repository import SessionRepository
from auth.domain.session.session import Session
from auth.domain.session.session_id import SessionId
from auth.domain.shared.domain_event import DomainEventAdder
from auth.domain.user.value_objects import UserId
from auth.infrastructure.persistence.sqlalchemy.tables import SESSIONS_TABLE


class SqlSessionRepositoryImpl(SessionRepository):
    def __init__(self, session: AsyncSession, event_adder: DomainEventAdder) -> None:
        self.__session = session
        self.__event_adder = event_adder

    def add(self, session: Session) -> None:
        self.__session.add(session)

    async def delete(self, session: Session) -> None:
        await self.__session.delete(session)

    async def with_session_id(self, session_id: SessionId) -> Session | None:
        stmt = select(Session).where(and_(SESSIONS_TABLE.c.session_id == session_id))
        result = (await self.__session.execute(stmt)).scalar_one_or_none()

        return self._load(result) if result else None

    async def with_user_id(self, user_id: UserId) -> list[Session]:
        stmt = select(Session).where(and_(SESSIONS_TABLE.c.user_id == user_id))
        result = (await self.__session.execute(stmt)).scalars().all()

        return [self._load(session) for session in result]

    def _load(self, session: Session) -> Session:
        object.__setattr__(session, "_event_adder", self.__event_adder)
        return session

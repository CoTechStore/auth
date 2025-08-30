from typing import Unpack

from sqlalchemy import and_, false, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.domain.shared.domain_event import DomainEventAdder
from auth.domain.user.repository import UserRepository
from auth.domain.user.specifications import UserSpecifications
from auth.domain.user.user import User
from auth.domain.user.value_objects import UserId
from auth.infrastructure.persistence.adapters.translators import UserTranslator
from auth.infrastructure.persistence.sqlalchemy.tables.user import USERS_TABLE


class SqlUserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession, event_adder: DomainEventAdder) -> None:
        self.__session = session
        self.__event_adder = event_adder

    def add(self, user: User) -> None:
        """Добавление пользователя."""
        self.__session.add(user)

    async def delete(self, user: User) -> None:
        """Удаление пользователя."""
        await self.__session.delete(user)

    async def find(self, **specifications: Unpack[UserSpecifications]) -> User | None:
        translator = UserTranslator(specifications)
        conditions = translator.specifications_mapping()

        query = select(User).where(and_(*conditions))

        user = (await self.__session.execute(query)).scalar_one_or_none()

        return self.__load(user) if user else None

    async def with_user_id(self, user_id: UserId) -> User | None:
        """Получить пользователя по user_id."""
        query = select(User).where(and_(USERS_TABLE.c.user_id == user_id))
        user = (await self.__session.execute(query)).scalar_one_or_none()

        return self.__load(user) if user else None

    async def with_login(self, login: str) -> User | None:
        """Проверка существования текущего логина."""
        query = select(User).where(
            and_(
                USERS_TABLE.c.login.ilike(f"%{login}%"),
                USERS_TABLE.c.hidden == false(),
            )
        )
        user = (await self.__session.execute(query)).scalar_one_or_none()
        return self.__load(user) if user else None

    def __load(self, user: User) -> User:
        object.__setattr__(user, "_event_adder", self.__event_adder)
        return user

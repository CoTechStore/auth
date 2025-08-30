from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from auth.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from auth.infrastructure.persistence.sqlalchemy.engine import (
    build_engine,
    build_session_maker,
    connect_session,
)


class WebPersistenceProvider(Provider):
    """Провайдер для PostgreSQL."""

    scope = Scope.APP

    @provide
    async def provide_postgres_engine(
        self, config: PostgresConfig
    ) -> AsyncIterable[AsyncEngine]:
        """Создание асинхронного движка для PostgreSQL."""
        async for engine in build_engine(config):
            yield engine

    @provide
    def provide_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        """Создание асинхронного сеанса PostgreSQL."""
        return build_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def provide_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        """Создание асинхронной сессии."""
        async for session in connect_session(session_maker):
            yield session

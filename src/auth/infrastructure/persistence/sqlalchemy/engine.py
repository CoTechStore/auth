from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from auth.infrastructure.persistence.sqlalchemy.config import PostgresConfig


async def build_engine(config: PostgresConfig) -> AsyncGenerator[AsyncEngine]:
    """Создание асинхронного движка для PostgreSQL."""
    engine = create_async_engine(config.uri)
    yield engine
    await engine.dispose()


def build_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Создание асинхронной фабрики сессий."""
    return async_sessionmaker(bind=engine, expire_on_commit=False)


async def connect_session(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """Создание асинхронного подключения к PostgreSQL."""
    async with session_maker() as session:
        yield session

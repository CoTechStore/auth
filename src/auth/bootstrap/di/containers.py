from alembic.config import Config as AlembicConfig
from dishka import AsyncContainer, Container, make_async_container, make_container
from dishka.integrations.fastapi import FastapiProvider
from structlog.stdlib import BoundLogger
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from auth.bootstrap.config import AuthConfig
from auth.bootstrap.di.providers import (
    AuthProvider,
    CliConfigProvider,
    WebApplicationAdaptersProvider,
    WebConfigProvider,
    WebDomainAdaptersProvider,
    WebHandlersProvider,
    WebMediatorProvider,
    WebPersistenceProvider,
)
from auth.infrastructure.persistence.sqlalchemy.config import PostgresConfig


def web_container(
    postgres_config: PostgresConfig, auth_config: AuthConfig, logger: BoundLogger
) -> AsyncContainer:
    """Создание контейнера для API."""
    return make_async_container(
        WebMediatorProvider(),
        FastapiProvider(),
        WebConfigProvider(),
        WebPersistenceProvider(),
        WebDomainAdaptersProvider(),
        WebApplicationAdaptersProvider(),
        WebHandlersProvider(),
        AuthProvider(),
        context={
            PostgresConfig: postgres_config,
            AuthConfig: auth_config,
            BoundLogger: logger,
        },
    )


def cli_container(
    alembic_config: AlembicConfig,
    uvicorn_config: UvicornConfig,
    uvicorn_server: UvicornServer,
) -> Container:
    """Создание контейнера для CLI."""
    return make_container(
        CliConfigProvider(),
        context={
            UvicornConfig: uvicorn_config,
            UvicornServer: uvicorn_server,
            AlembicConfig: alembic_config,
        },
    )

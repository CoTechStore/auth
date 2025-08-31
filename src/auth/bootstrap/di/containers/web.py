from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider
from structlog.stdlib import BoundLogger

from auth.bootstrap.config import AuthConfig
from auth.bootstrap.di.providers.common import MediatorProvider, PersistenceProvider
from auth.bootstrap.di.providers.web import (
    ApplicationAdaptersProvider,
    AuthProvider,
    DomainAdaptersProvider,
    HandlersProvider,
    WebConfigProvider,
)
from auth.infrastructure.persistence.sqlalchemy.config import PostgresConfig


def web_container(
    postgres_config: PostgresConfig, auth_config: AuthConfig, logger: BoundLogger
) -> AsyncContainer:
    """Создание контейнера для API."""
    return make_async_container(
        MediatorProvider(),
        WebConfigProvider(),
        PersistenceProvider(),
        DomainAdaptersProvider(),
        ApplicationAdaptersProvider(),
        HandlersProvider(),
        AuthProvider(),
        FastapiProvider(),
        context={
            PostgresConfig: postgres_config,
            AuthConfig: auth_config,
            BoundLogger: logger,
        },
    )

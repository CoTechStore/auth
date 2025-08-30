from alembic.config import Config as AlembicConfig
from dishka import Provider, Scope, from_context
from structlog.stdlib import BoundLogger
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from auth.bootstrap.config import AuthConfig
from auth.infrastructure.persistence.sqlalchemy.config import PostgresConfig


class WebConfigProvider(Provider):
    """Провайдер конфигураций приложения."""

    scope = Scope.APP

    postgres_config = from_context(PostgresConfig)
    logger = from_context(BoundLogger)
    auth_config = from_context(AuthConfig)


class CliConfigProvider(Provider):
    """Провайдер конфигураций для cli-команд."""

    scope = Scope.APP

    alembic_config = from_context(AlembicConfig)
    uvicorn_config = from_context(UvicornConfig)
    uvicorn_server = from_context(UvicornServer)

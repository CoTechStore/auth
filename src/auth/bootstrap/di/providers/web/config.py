from dishka import Provider, Scope, from_context
from structlog.stdlib import BoundLogger

from auth.bootstrap.config import AuthConfig
from auth.infrastructure.persistence.sqlalchemy.config import PostgresConfig


class WebConfigProvider(Provider):
    """Провайдер конфигураций приложения."""

    scope = Scope.APP

    postgres_config = from_context(PostgresConfig)
    logger = from_context(BoundLogger)
    auth_config = from_context(AuthConfig)

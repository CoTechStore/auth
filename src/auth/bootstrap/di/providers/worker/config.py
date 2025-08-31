from dishka import Provider, Scope, from_context
from faststream.rabbit import RabbitBroker
from structlog.stdlib import BoundLogger

from auth.infrastructure.outbox.config import RabbitConfig
from auth.infrastructure.persistence.sqlalchemy.config import PostgresConfig


class WorkerConfigProvider(Provider):
    scope = Scope.APP

    rabbit_broker = from_context(RabbitBroker)
    rabbit_config = from_context(RabbitConfig)
    postgres_config = from_context(PostgresConfig)
    logger = from_context(BoundLogger)

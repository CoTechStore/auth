from dishka import AsyncContainer, make_async_container
from dishka.integrations.taskiq import TaskiqProvider
from faststream.rabbit import RabbitBroker
from structlog.stdlib import BoundLogger

from auth.bootstrap.di.providers.common import MediatorProvider, PersistenceProvider
from auth.bootstrap.di.providers.worker import (
    BrokerProvider,
    OutboxProvider,
    WorkerConfigProvider,
)
from auth.infrastructure.outbox.config import RabbitConfig
from auth.infrastructure.persistence.sqlalchemy.config import PostgresConfig


def worker_container(
    rabbit_broker: RabbitBroker,
    rabbit_config: RabbitConfig,
    postgres_config: PostgresConfig,
    logger: BoundLogger,
) -> AsyncContainer:
    """Создание контейнера для фоновых задач."""
    return make_async_container(
        TaskiqProvider(),
        BrokerProvider(),
        OutboxProvider(),
        MediatorProvider(),
        WorkerConfigProvider(),
        PersistenceProvider(),
        context={
            RabbitBroker: rabbit_broker,
            RabbitConfig: rabbit_config,
            PostgresConfig: postgres_config,
            BoundLogger: logger,
        },
    )

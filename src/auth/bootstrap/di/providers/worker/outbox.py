from dishka import Provider, Scope, alias, provide
from sqlalchemy.ext.asyncio import AsyncSession
from structlog.stdlib import BoundLogger

from auth.application.ports import Logger
from auth.infrastructure.messaging.outbox.interfaces import OutboxGateway, OutboxPublisher
from auth.infrastructure.messaging.outbox.outbox_processor import OutboxProcessor
from auth.infrastructure.messaging.outbox.outbox_publisher import RabbitMQOutboxPublisher
from auth.infrastructure.messaging.outbox.sql_outbox_gateway import SqlOutboxGatewayImpl
from auth.infrastructure.messaging.transaction import Transaction


class OutboxProvider(Provider):
    scope = Scope.REQUEST

    outbox_gateway = provide(SqlOutboxGatewayImpl, provides=OutboxGateway)
    outbox_publisher = provide(
        RabbitMQOutboxPublisher, provides=OutboxPublisher, scope=Scope.APP
    )
    outbox_processor = provide(OutboxProcessor)

    transaction = alias(AsyncSession, provides=Transaction)
    logger = alias(BoundLogger, provides=Logger)

from dishka import Provider, Scope, alias, provide
from sqlalchemy.ext.asyncio import AsyncSession

from auth.infrastructure.messaging.outbox.interfaces import OutboxGateway, OutboxPublisher
from auth.infrastructure.messaging.outbox.outbox_processor import OutboxProcessor
from auth.infrastructure.messaging.outbox.outbox_publisher import RabbitMQOutboxPublisher
from auth.infrastructure.messaging.transaction import Transaction
from auth.infrastructure.persistence.adapters import SqlOutboxGatewayImpl


class OutboxProvider(Provider):
    scope = Scope.REQUEST

    outbox_gateway = provide(SqlOutboxGatewayImpl, provides=OutboxGateway)
    outbox_publisher = provide(
        RabbitMQOutboxPublisher, provides=OutboxPublisher, scope=Scope.APP
    )
    outbox_processor = provide(OutboxProcessor)

    transaction = alias(AsyncSession, provides=Transaction)

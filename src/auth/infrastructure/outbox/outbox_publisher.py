from enum import StrEnum

from faststream.rabbit import RabbitBroker

from auth.infrastructure.outbox.interfaces import OutboxPublisher
from auth.infrastructure.outbox.outbox_message import OutboxMessage


class ExchangeName(StrEnum):
    AUTH = "auth"


class RabbitMQOutboxPublisher(OutboxPublisher):
    def __init__(self, broker: RabbitBroker) -> None:
        self.__broker = broker

    async def publish(self, message: OutboxMessage) -> None:
        await self.__broker.publish(
            routing_key=message.event_type,
            message_id=str(message.message_id),
            message=message.data,
        )

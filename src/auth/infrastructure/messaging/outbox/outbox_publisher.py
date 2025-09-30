from faststream.rabbit import RabbitBroker

from auth.application.ports import Logger
from auth.infrastructure.messaging.config import ExchangeName, QueueName
from auth.infrastructure.messaging.outbox.interfaces import OutboxPublisher
from auth.infrastructure.messaging.outbox.outbox_message import OutboxMessage


class RabbitMQOutboxPublisher(OutboxPublisher):
    def __init__(self, broker: RabbitBroker, logger: Logger) -> None:
        self.__broker = broker
        self.__logger = logger

    async def publish(self, message: OutboxMessage) -> None:
        await self.__broker.publish(
            routing_key=message.event_type,
            message_id=str(message.message_id),
            message=message.data,
            exchange=ExchangeName.AUTH,
            queue=QueueName.AUTH,
        )

        await self.__logger.ainfo(
            event=f"Published event {message.event_type} in queue {QueueName.AUTH}.",
            message_id=message.message_id,
        )

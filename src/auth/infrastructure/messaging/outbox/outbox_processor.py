from auth.infrastructure.messaging.outbox.interfaces import OutboxGateway, OutboxPublisher
from auth.infrastructure.messaging.transaction import Transaction


class OutboxProcessor:
    """Класс читающий события находящиеся в таблице Outbox."""

    def __init__(
        self,
        transaction: Transaction,
        outbox_gateway: OutboxGateway,
        outbox_publisher: OutboxPublisher,
    ) -> None:
        self.__transaction = transaction
        self.__outbox_gateway = outbox_gateway
        self.__outbox_publisher = outbox_publisher

    async def process(self) -> None:
        messages = await self.__outbox_gateway.select()

        for message in messages:
            await self.__outbox_publisher.publish(message)
            await self.__outbox_gateway.delete(message)

        await self.__transaction.commit()

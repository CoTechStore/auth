from typing import cast

from auth.domain.shared.domain_event import DomainEvent, EventHandler
from auth.domain.shared.event_id import EventId
from auth.infrastructure.messaging.outbox.interfaces import OutboxGateway
from auth.infrastructure.messaging.outbox.outbox_message import OutboxMessage
from auth.infrastructure.messaging.serialization import to_json


class OutboxHandler(EventHandler[DomainEvent]):
    def __init__(self, outbox_gateway: OutboxGateway) -> None:
        self.__outbox_gateway = outbox_gateway

    async def handle(self, event: DomainEvent) -> None:
        message = OutboxMessage(
            message_id=cast(EventId, event.event_id),
            event_type=event.event_type,
            data=to_json(event),
        )
        await self.__outbox_gateway.add(message)

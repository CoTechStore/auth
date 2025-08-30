from typing import TYPE_CHECKING, cast

from auth.application.common.handlers import NotificationHandler
from auth.domain.shared.domain_event import DomainEvent
from auth.infrastructure.outbox.interfaces import OutboxGateway
from auth.infrastructure.outbox.outbox_message import OutboxMessage
from auth.infrastructure.outbox.outbox_serialization import to_json

if TYPE_CHECKING:
    from auth.domain.shared.event_id import EventId


class OutboxHandler(NotificationHandler[DomainEvent]):
    def __init__(self, outbox_gateway: OutboxGateway) -> None:
        self.__outbox_gateway = outbox_gateway

    async def handle(self, notification: DomainEvent) -> None:
        message = OutboxMessage(
            message_id=cast("EventId", notification.event_id),
            event_type=notification.event_type,
            data=to_json(notification),
        )
        await self.__outbox_gateway.add(message)

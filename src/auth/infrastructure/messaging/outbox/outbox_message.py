from dataclasses import dataclass

from auth.domain.shared.event_id import EventId


@dataclass(frozen=True)
class OutboxMessage:
    message_id: EventId
    event_type: str
    data: str

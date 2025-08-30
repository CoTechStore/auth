from uuid6 import uuid7

from auth.application.ports import IdGenerator
from auth.domain.session.session_id import SessionId
from auth.domain.shared.event_id import EventId
from auth.domain.user.value_objects import UserId


class IdGeneratorImpl(IdGenerator):
    """Реализация генератора уникальных идентификаторов."""

    def generate_user_id(self) -> UserId:
        return UserId(uuid7())

    def generate_session_id(self) -> SessionId:
        return SessionId(uuid7())

    def generate_event_id(self) -> EventId:
        return EventId(uuid7())

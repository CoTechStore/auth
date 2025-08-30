from abc import ABC, abstractmethod

from auth.domain.session.session_id import SessionId
from auth.domain.shared.event_id import EventId
from auth.domain.user.value_objects import UserId


class IdGenerator(ABC):
    @abstractmethod
    def generate_user_id(self) -> UserId: ...

    @abstractmethod
    def generate_session_id(self) -> SessionId: ...

    @abstractmethod
    def generate_event_id(self) -> EventId: ...

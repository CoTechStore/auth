from datetime import datetime

from auth.domain.session.session_id import SessionId
from auth.domain.shared.domain_event import DomainEventAdder
from auth.domain.shared.entity import Entity, EventTrackableEntity
from auth.domain.user.value_objects import UserId


class Session(Entity[SessionId], EventTrackableEntity):
    def __init__(
        self,
        session_id: SessionId,
        event_adder: DomainEventAdder,
        *,
        user_id: UserId,
        expires_at: datetime,
        iat: datetime,
    ) -> None:
        Entity.__init__(self, session_id)
        EventTrackableEntity.__init__(self, event_adder)
        self._user_id = user_id
        self._expires_at = expires_at
        self._iat = iat

    def prolong_expiration(self, expires_at: datetime) -> None:
        self._expires_at = expires_at

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def expires_at(self) -> datetime:
        return self._expires_at

    @property
    def iat(self) -> datetime:
        return self._iat

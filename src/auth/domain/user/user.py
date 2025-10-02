from auth.domain.shared.domain_event import DomainEventAdder
from auth.domain.shared.entity import Entity, EventTrackableEntity
from auth.domain.user.events import (
    UserPasswordChanged,
)
from auth.domain.user.user_type import UserType
from auth.domain.user.value_objects import Username, UserId


class User(Entity[UserId], EventTrackableEntity):
    def __init__(
        self,
        user_id: UserId,
        event_adder: DomainEventAdder,
        *,
        username: Username,
        hash_password: bytes,
        is_active: bool = True,
        user_type: UserType = UserType.DEFAULT_USER,
    ) -> None:
        Entity.__init__(self, entity_id=user_id)
        EventTrackableEntity.__init__(self, event_adder=event_adder)

        self._username = username
        self._hash_password = hash_password
        self._is_active = is_active
        self._user_type = user_type

    def change_password(self, hash_password: bytes) -> None:
        self._hash_password = hash_password

        self.track_event(
            event=UserPasswordChanged(
                user_id=self.entity_id, hash_password=self._hash_password
            )
        )

    @property
    def username_vo(self) -> Username:
        return self._username

    @property
    def hash_password(self) -> bytes:
        return self._hash_password

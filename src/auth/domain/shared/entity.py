from abc import ABC
from collections.abc import Hashable
from typing import NoReturn

from auth.domain.shared.domain_event import DomainEvent, DomainEventAdder


class Entity[TEntityId: Hashable]:
    def __init__(self, entity_id: TEntityId) -> None:
        self._entity_id = entity_id

    @property
    def entity_id(self) -> TEntityId:
        return self._entity_id

    @entity_id.setter
    def entity_id(self, identity: TEntityId) -> NoReturn:
        raise AttributeError("The entity ID cannot be changed.")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented

        return bool(other.entity_id == self.entity_id)

    def __hash__(self) -> int:
        return hash(self.entity_id)


class EventTrackableEntity(ABC):
    """The base class for tracking events."""

    def __init__(self, event_adder: DomainEventAdder) -> None:
        self._event_adder = event_adder

    def track_event(self, event: DomainEvent) -> None:
        self._event_adder.add_event(event)

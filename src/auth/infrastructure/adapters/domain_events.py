from collections.abc import Iterable

from auth.application.ports import DomainEventsRaiser
from auth.domain.shared.domain_event import DomainEvent, DomainEventAdder


class DomainEventsImpl(DomainEventAdder, DomainEventsRaiser):
    def __init__(self) -> None:
        self.__events: list[DomainEvent] = []

    def add_event(self, event: DomainEvent) -> None:
        self.__events.append(event)

    def raise_events(self) -> Iterable[DomainEvent]:
        events = tuple(self.__events)
        self.__events.clear()

        return events

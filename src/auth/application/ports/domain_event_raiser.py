from abc import ABC, abstractmethod
from collections.abc import Iterable

from auth.domain.shared.domain_event import DomainEvent


class DomainEventsRaiser(ABC):
    @abstractmethod
    def raise_events(self) -> Iterable[DomainEvent]: ...

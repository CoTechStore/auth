from abc import ABC, abstractmethod

from auth.domain.shared.domain_event import DomainEvent


class Publisher(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None: ...

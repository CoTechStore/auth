from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from auth.domain.shared.event_id import EventId


@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    """Базовый класс доменных событий."""

    event_id: EventId | None = field(default=None, init=False)
    event_date: datetime | None = field(default=None, init=False)

    @property
    def event_type(self) -> str:
        """Возвращает имя класса события."""
        return self.__class__.__name__

    def set_event_id(self, event_id: EventId) -> None:
        """Установить идентификационный номер события."""
        if self.event_id:
            return

        object.__setattr__(self, "event_id", event_id)

    def set_event_date(self, event_date: datetime) -> None:
        """Установить дату и время создания события."""
        if self.event_date:
            return

        object.__setattr__(self, "event_date", event_date)


class DomainEventAdder(ABC):
    @abstractmethod
    def add_event(self, event: DomainEvent) -> None: ...


class EventHandler[TDomainEvent: DomainEvent](ABC):
    @abstractmethod
    async def handle(self, event: TDomainEvent) -> None: ...

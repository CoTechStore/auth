from abc import ABC, abstractmethod

from auth.domain.shared.markers import Notification


class Publisher(ABC):
    @abstractmethod
    async def publish(self, notification: Notification) -> None: ...

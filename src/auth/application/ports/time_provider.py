from abc import ABC, abstractmethod
from datetime import datetime


class TimeProvider(ABC):
    @abstractmethod
    def current_time(self) -> datetime: ...

    @abstractmethod
    def unix_time(self, current_time: datetime) -> int: ...

    @abstractmethod
    def access_token_expires(self, current_time: datetime) -> datetime: ...

    @abstractmethod
    def refresh_token_expires(self, current_time: datetime) -> datetime: ...

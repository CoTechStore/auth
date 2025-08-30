from abc import ABC, abstractmethod
from typing import Any


class Logger(ABC):
    @abstractmethod
    def info(self, event: str | None = None, *args: Any, **kw: Any) -> Any: ...

    @abstractmethod
    def warning(self, event: str | None = None, *args: Any, **kw: Any) -> Any: ...

    @abstractmethod
    def error(self, event: str | None = None, *args: Any, **kw: Any) -> Any: ...

    @abstractmethod
    def exception(self, event: str | None = None, *args: Any, **kw: Any) -> Any: ...

from abc import ABC, abstractmethod
from typing import Any


class Logger(ABC):
    @abstractmethod
    async def ainfo(self, event: str | None = None, *args: Any, **kw: Any) -> Any: ...

    @abstractmethod
    async def awarning(self, event: str | None = None, *args: Any, **kw: Any) -> Any: ...

    @abstractmethod
    async def aerror(self, event: str | None = None, *args: Any, **kw: Any) -> Any: ...

    @abstractmethod
    async def aexception(
        self, event: str | None = None, *args: Any, **kw: Any
    ) -> Any: ...

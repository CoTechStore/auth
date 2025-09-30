from abc import ABC, abstractmethod
from collections.abc import Callable, Coroutine
from typing import Any

from auth.application.common.markers import BaseRequest
from auth.domain.shared.domain_event import DomainEvent

type HandleNext[TRequest: BaseRequest | DomainEvent, TResponse] = Callable[
    [TRequest], Coroutine[Any, Any, TResponse]
]


class RequestHandler[TRequest: BaseRequest[Any], TResponse](ABC):
    @abstractmethod
    async def handle(self, request: TRequest) -> TResponse: ...


class PipelineBehaviorHandler[TRequest: BaseRequest[Any] | DomainEvent, TResponse](ABC):
    @abstractmethod
    async def handle(
        self, request: TRequest, handle_next: HandleNext[TRequest, TResponse]
    ) -> TResponse: ...


class CommandHandler[TRequest: BaseRequest[Any], TResponse](
    RequestHandler[TRequest, TResponse]
):
    @abstractmethod
    async def handle(self, command: TRequest) -> TResponse: ...


class QueryHandler[TRequest: BaseRequest[Any], TResponse](
    RequestHandler[TRequest, TResponse]
):
    @abstractmethod
    async def handle(self, query: TRequest) -> TResponse: ...

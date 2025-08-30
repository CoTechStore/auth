import functools
from collections.abc import Iterable
from typing import cast

from auth.application.common.handlers import (
    HandleNext,
    NotificationHandler,
    PipelineBehaviorHandler,
    RequestHandler,
)
from auth.application.common.markers import BaseRequest
from auth.domain.shared.markers import Notification
from auth.infrastructure.mediator.interfaces import Chain


class ChainImpl(Chain):
    """Класс собирающий цепочку поведений."""

    def build_pipeline_behaviors(
        self,
        handler: RequestHandler | NotificationHandler,
        behaviors: Iterable[PipelineBehaviorHandler],
    ) -> HandleNext:
        """
        Паттерн Chain of Responsibility.
        Добавление дополнительных поведений к обработчику.
        """
        handle_next: HandleNext = handler.handle

        for behavior in behaviors:
            handle_next = self._wrap_with_behavior(behavior, handle_next)

        return handle_next

    @staticmethod
    def _wrap_with_behavior(
        behavior: PipelineBehaviorHandler,
        handle_next: HandleNext,
    ) -> HandleNext:
        @functools.wraps(handle_next)
        async def wrapped_handler[TResponse](
            request: BaseRequest | Notification,
        ) -> TResponse:
            """Декоратор выполняющий поведение поверх обработчика."""
            return cast(TResponse, await behavior.handle(request, handle_next))

        return wrapped_handler

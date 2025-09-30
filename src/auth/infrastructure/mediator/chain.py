import functools
from collections.abc import Iterable
from typing import cast

from auth.application.common.handlers import (
    HandleNext,
    PipelineBehaviorHandler,
    RequestHandler,
)
from auth.application.common.markers import BaseRequest
from auth.domain.shared.domain_event import EventHandler, DomainEvent
from auth.infrastructure.mediator.interfaces import Chain


class ChainImpl(Chain):
    """A class that collects a chain of behaviors."""

    def build_pipeline_behaviors(
        self,
        handler: RequestHandler | EventHandler,
        behaviors: Iterable[PipelineBehaviorHandler],
    ) -> HandleNext:
        """
        Chain of Responsibility pattern.
        Adding additional behaviors to the handler.
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
            request: BaseRequest | DomainEvent,
        ) -> TResponse:
            """Execute behavior on top of a handler."""
            return cast(TResponse, await behavior.handle(request, handle_next))

        return wrapped_handler

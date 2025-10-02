from auth.application.common.markers import BaseRequest
from auth.application.ports import Publisher
from auth.domain.shared.domain_event import DomainEvent
from auth.infrastructure.errors import HandlerNotFoundError
from auth.infrastructure.mediator.interfaces import Chain, Resolver
from auth.infrastructure.mediator.registry import Registry
from auth.presentation.sender import Sender


class MediatorImpl(Sender, Publisher):
    """Class that implements the Mediator design pattern."""

    def __init__(self, resolver: Resolver, registry: Registry, chain: Chain) -> None:
        self.__resolver = resolver
        self.__registry = registry
        self.__chain = chain

    async def send[TResponse](self, request: BaseRequest[TResponse]) -> TResponse:
        """Send request."""
        request_type = type(request)
        handler_class = self.__registry.get_request_handler(request_type)

        if not handler_class:
            raise HandlerNotFoundError(
                f"Not found handler for '{request_type.__name__}'."
            )

        # We get the notification handler from the dependency container.
        handler = await self.__resolver.resolve(handler_class)

        # Adding additional behaviors.
        behaviors = [
            await self.__resolver.resolve(behavior_type)
            for behavior_type in self.__registry.get_pipeline_behaviors(request_type)
        ]
        # We're building a chain of behaviors.
        handle_next = self.__chain.build_pipeline_behaviors(handler, behaviors)

        result: TResponse = await handle_next(request)
        return result

    async def publish(self, event: DomainEvent) -> None:
        """Send a notification about the event."""
        event_type = type(event)
        handler_classes = self.__registry.get_event_handlers(event_type)

        for handler_class in handler_classes:
            # We get the notification handler from the dependency container.
            handler = await self.__resolver.resolve(handler_class)

            # Adding additional behaviors.
            behaviors = [
                await self.__resolver.resolve(behavior_type)
                for behavior_type in self.__registry.get_pipeline_behaviors(event_type)
            ]
            # We're building a chain of behaviors.
            handle_next = self.__chain.build_pipeline_behaviors(handler, behaviors)

            await handle_next(event)

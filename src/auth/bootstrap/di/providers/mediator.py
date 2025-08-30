from dishka import AnyOf, Provider, Scope, provide

from auth.application.common.behaviors import (
    CommitionBehaviorHandler,
    EventPublishingBehaviorHandler,
    LogErrorBehaviorHandler,
)
from auth.application.common.markers import BaseRequest, Command
from auth.application.operations.commands import (
    LoginCommand,
    LoginHandler,
    LogoutCommand,
    LogoutHandler,
)
from auth.application.ports import Publisher
from auth.domain.shared.domain_event import DomainEvent
from auth.infrastructure.mediator.chain import ChainImpl
from auth.infrastructure.mediator.interfaces import Chain, Resolver
from auth.infrastructure.mediator.mediator import MediatorImpl
from auth.infrastructure.mediator.registry import Registry
from auth.infrastructure.mediator.resolvers import DishkaResolver
from auth.infrastructure.outbox.outbox_handler import OutboxHandler
from auth.presentation.sender import Sender


class WebMediatorProvider(Provider):
    """Провайдер медиатора."""

    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def provide_registry(self) -> Registry:
        registry = Registry()

        registry.add_request_handler(LoginCommand, LoginHandler)
        registry.add_request_handler(LogoutCommand, LogoutHandler)

        registry.add_pipeline_behavior_handlers(BaseRequest, LogErrorBehaviorHandler)
        registry.add_pipeline_behavior_handlers(
            Command, EventPublishingBehaviorHandler, CommitionBehaviorHandler
        )

        registry.add_notification_handlers(DomainEvent, OutboxHandler)

        return registry

    mediator = provide(MediatorImpl, provides=AnyOf[Sender, Publisher])
    resolver = provide(DishkaResolver, provides=Resolver)
    chain = provide(ChainImpl, provides=Chain)

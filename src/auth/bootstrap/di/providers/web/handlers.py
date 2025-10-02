from dishka import Provider, Scope, provide_all

from auth.application.common.behaviors import (
    CommitionBehaviorHandler,
    EventPublishingBehaviorHandler,
    LogErrorBehaviorHandler,
)
from auth.application.operations.commands import (
    LoginHandler,
    LogoutHandler,
    RegisterHandler,
)
from auth.infrastructure.messaging.outbox.outbox_handler import OutboxHandler


class HandlersProvider(Provider):
    """Провайдер обработчиков."""

    scope = Scope.REQUEST

    command_handlers = provide_all(
        LoginHandler,
        LogoutHandler,
        RegisterHandler,
    )

    event_handlers = provide_all(
        OutboxHandler,
    )

    # query_handlers = provide_all()

    behavior_handlers = provide_all(
        CommitionBehaviorHandler,
        EventPublishingBehaviorHandler,
        LogErrorBehaviorHandler,
    )

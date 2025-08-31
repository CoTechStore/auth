from dishka import Provider, Scope, provide_all

from auth.application.common.behaviors import (
    CommitionBehaviorHandler,
    EventPublishingBehaviorHandler,
    LogErrorBehaviorHandler,
)
from auth.application.operations.commands import LoginHandler, LogoutHandler


class HandlersProvider(Provider):
    """Провайдер обработчиков."""

    scope = Scope.REQUEST

    command_handlers = provide_all(
        LoginHandler,
        LogoutHandler,
    )

    # query_handlers = provide_all()

    behavior_handlers = provide_all(
        CommitionBehaviorHandler,
        EventPublishingBehaviorHandler,
        LogErrorBehaviorHandler,
    )

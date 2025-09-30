from auth.application.common.handlers import (
    PipelineBehaviorHandler,
    RequestHandler,
)
from auth.application.common.markers import BaseRequest
from auth.domain.shared.domain_event import EventHandler, DomainEvent


class Registry:
    """Регистрация обработчиков и поведений."""

    __request_handlers: dict[type[BaseRequest], type[RequestHandler]]
    __event_handlers: dict[type[DomainEvent], list[type[EventHandler]]]
    __pipeline_behaviors: dict[
        type[BaseRequest] | type[DomainEvent], list[type[PipelineBehaviorHandler]]
    ]

    def __init__(self) -> None:
        self.__request_handlers = {}
        self.__event_handlers = {}
        self.__pipeline_behaviors = {}

    def add_request_handler(
        self,
        request_type: type[BaseRequest],
        request_handler: type[RequestHandler],
    ) -> None:
        """Добавить обработчик запроса."""
        self.__request_handlers[request_type] = request_handler

    def add_event_handlers(
        self,
        notification_type: type[DomainEvent],
        *notification_handlers: type[EventHandler],
    ) -> None:
        """Добавить обработчик уведомления."""
        self.__event_handlers.setdefault(notification_type, []).extend(
            notification_handlers,
        )

    def add_pipeline_behavior_handlers(
        self,
        request_type: type[BaseRequest] | type[DomainEvent],
        *pipeline_behaviors: type[PipelineBehaviorHandler],
    ) -> None:
        """Добавить поведение для запроса."""
        self.__pipeline_behaviors.setdefault(request_type, []).extend(pipeline_behaviors)

    def get_request_handler(
        self, request_type: type[BaseRequest]
    ) -> type[RequestHandler] | None:
        """Получить обработчик запроса."""
        return self.__request_handlers.get(request_type)

    def get_event_handlers(
        self, event_type: type[DomainEvent]
    ) -> list[type[EventHandler]]:
        """Получить обработчики уведомления."""
        return [
            handler
            for event, handlers in self.__event_handlers.items()
            for handler in handlers
            if issubclass(event_type, event)
        ]

    def get_pipeline_behaviors(
        self, request_type: type[BaseRequest] | type[DomainEvent]
    ) -> list[type[PipelineBehaviorHandler]]:
        """Получить поведения для запроса."""
        return [
            behavior
            for request, behaviors in self.__pipeline_behaviors.items()
            for behavior in behaviors
            if issubclass(request_type, request)
        ]

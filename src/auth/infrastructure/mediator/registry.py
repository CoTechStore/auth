from auth.application.common.handlers import (
    NotificationHandler,
    PipelineBehaviorHandler,
    RequestHandler,
)
from auth.application.common.markers import BaseRequest
from auth.domain.shared.markers import Notification


class Registry:
    """Регистрация обработчиков и поведений."""

    __request_handlers: dict[type[BaseRequest], type[RequestHandler]]
    __notification_handlers: dict[type[Notification], list[type[NotificationHandler]]]
    __pipeline_behaviors: dict[
        type[BaseRequest] | type[Notification], list[type[PipelineBehaviorHandler]]
    ]

    def __init__(self) -> None:
        self.__request_handlers = {}
        self.__notification_handlers = {}
        self.__pipeline_behaviors = {}

    def add_request_handler(
        self,
        request_type: type[BaseRequest],
        request_handler: type[RequestHandler],
    ) -> None:
        """Добавить обработчик запроса."""
        self.__request_handlers[request_type] = request_handler

    def add_notification_handlers(
        self,
        notification_type: type[Notification],
        *notification_handlers: type[NotificationHandler],
    ) -> None:
        """Добавить обработчик уведомления."""
        self.__notification_handlers.setdefault(notification_type, []).extend(
            notification_handlers,
        )

    def add_pipeline_behavior_handlers(
        self,
        request_type: type[BaseRequest] | type[Notification],
        *pipeline_behaviors: type[PipelineBehaviorHandler],
    ) -> None:
        """Добавить поведение для запроса."""
        self.__pipeline_behaviors.setdefault(request_type, []).extend(pipeline_behaviors)

    def get_request_handler(
        self, request_type: type[BaseRequest]
    ) -> type[RequestHandler] | None:
        """Получить обработчик запроса."""
        return self.__request_handlers.get(request_type)

    def get_notification_handlers(
        self, notification_type: type[Notification]
    ) -> list[type[NotificationHandler]]:
        """Получить обработчики уведомления."""
        return [
            handler
            for notification, handlers in self.__notification_handlers.items()
            for handler in handlers
            if issubclass(notification_type, notification)
        ]

    def get_pipeline_behaviors(
        self, request_type: type[BaseRequest] | type[Notification]
    ) -> list[type[PipelineBehaviorHandler]]:
        """Получить поведения для запроса."""
        return [
            behavior
            for request, behaviors in self.__pipeline_behaviors.items()
            for behavior in behaviors
            if issubclass(request_type, request)
        ]

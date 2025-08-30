from auth.application.common.markers import BaseRequest
from auth.application.ports import Publisher
from auth.domain.shared.markers import Notification
from auth.infrastructure.errors import HandlerNotFoundError
from auth.infrastructure.mediator.interfaces import Chain, Resolver
from auth.infrastructure.mediator.registry import Registry
from auth.presentation.sender import Sender


class MediatorImpl(Sender, Publisher):
    """Класс-корень реализующий паттерн проектирования Mediator."""

    def __init__(self, resolver: Resolver, registry: Registry, chain: Chain) -> None:
        self.__resolver = resolver
        self.__registry = registry
        self.__chain = chain

    async def send[TResponse](self, request: BaseRequest[TResponse]) -> TResponse:
        """Отправить запрос."""
        request_type = type(request)
        handler_class = self.__registry.get_request_handler(request_type)

        if not handler_class:
            raise HandlerNotFoundError(
                f"Обработчик для '{request_type.__name__}' не найден."
            )

        # Получаем обработчик уведомления из контейнера зависимостей.
        handler = await self.__resolver.resolve(handler_class)

        # Добавляем дополнительные поведения.
        behaviors = [
            await self.__resolver.resolve(behavior_type)
            for behavior_type in self.__registry.get_pipeline_behaviors(request_type)
        ]
        # Собираем цепочку поведений.
        handle_next = self.__chain.build_pipeline_behaviors(handler, behaviors)

        result: TResponse = await handle_next(request)
        return result

    async def publish(self, notification: Notification) -> None:
        """Отправить уведомление о событии."""
        notification_type = type(notification)
        handler_classes = self.__registry.get_notification_handlers(notification_type)

        for handler_class in handler_classes:
            # Получаем обработчик уведомления из контейнера зависимостей.
            handler = await self.__resolver.resolve(handler_class)

            # Добавляем дополнительные поведения.
            behaviors = [
                await self.__resolver.resolve(behavior_type)
                for behavior_type in self.__registry.get_pipeline_behaviors(
                    notification_type
                )
            ]
            # Собираем цепочку поведений.
            handle_next = self.__chain.build_pipeline_behaviors(handler, behaviors)

            await handle_next(notification)

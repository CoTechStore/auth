from auth.application.common.handlers import HandleNext, PipelineBehaviorHandler
from auth.application.common.markers import Command
from auth.application.ports import IdGenerator, Publisher, TimeProvider
from auth.application.ports.domain_event_raiser import DomainEventsRaiser


class EventPublishingBehaviorHandler[TCommand: Command, TResponse](
    PipelineBehaviorHandler[TCommand, TResponse]
):
    def __init__(
        self,
        publisher: Publisher,
        events_raiser: DomainEventsRaiser,
        id_generator: IdGenerator,
        time_provider: TimeProvider,
    ) -> None:
        self.__publisher = publisher
        self.__events_raiser = events_raiser
        self.__id_generator = id_generator
        self.__time_provider = time_provider

    async def handle(
        self, request: TCommand, handle_next: HandleNext[TCommand, TResponse]
    ) -> TResponse:
        response = await handle_next(request)
        events = self.__events_raiser.raise_events()

        for event in events:
            event.set_event_id(self.__id_generator.generate_event_id())
            event.set_event_date(self.__time_provider.current_time())

            await self.__publisher.publish(event)

        return response

from dishka import Provider, Scope, provide
from faststream.rabbit import RabbitBroker

from auth.infrastructure.outbox.config import RabbitConfig


class BrokerProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_rabbit_broker(self, config: RabbitConfig) -> RabbitBroker:
        return RabbitBroker(config.uri)

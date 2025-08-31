from dishka import Provider, Scope, from_context
from taskiq_aio_pika import AioPikaBroker


class CliWorkerConfigProvider(Provider):
    """Провайдер конфигураций для cli-команд."""

    scope = Scope.APP

    aio_pika_broker = from_context(AioPikaBroker)

from dishka import Container, make_container
from taskiq_aio_pika import AioPikaBroker

from auth.bootstrap.di.providers.cli import CliWorkerConfigProvider


def cli_worker_container(taskiq_broker: AioPikaBroker) -> Container:
    """Создание контейнера для CLI."""
    return make_container(
        CliWorkerConfigProvider(),
        context={
            AioPikaBroker: taskiq_broker,
        },
    )

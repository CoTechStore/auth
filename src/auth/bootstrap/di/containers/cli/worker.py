from dishka import Container, make_container
from taskiq.cli.worker.args import WorkerArgs

from auth.bootstrap.di.providers.cli.worker import CliWorkerConfigProvider


def cli_worker_container(worker_args: WorkerArgs) -> Container:
    """Создание контейнера для CLI."""
    return make_container(
        CliWorkerConfigProvider(),
        context={
            WorkerArgs: worker_args,
        },
    )

from click import Context, group, pass_context
from dishka.integrations.click import setup_dishka
from taskiq_aio_pika import AioPikaBroker

from auth.bootstrap.config import get_config
from auth.bootstrap.di.containers.cli_worker import cli_worker_container
from auth.presentation.cli.commands.scheduler_start import start_scheduler
from auth.presentation.cli.commands.worker_start import start_worker


@group()
@pass_context
def main(context: Context) -> None:
    """Старт приложением через CLI."""
    rabbit_config = get_config().rabbit_config
    taskiq_broker = AioPikaBroker(url=rabbit_config.uri)
    container = cli_worker_container(taskiq_broker)
    setup_dishka(container, context, finalize_container=True)


main.command(start_worker)
main.command(start_scheduler)

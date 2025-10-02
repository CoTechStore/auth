from click import Context, group, pass_context
from dishka.integrations.click import setup_dishka
from taskiq.cli.worker.args import WorkerArgs

from auth.bootstrap.di.containers.cli.worker import cli_worker_container
from auth.presentation.cli.commands.worker_start import start_worker


@group()
@pass_context
def main(context: Context) -> None:
    """Старт приложением через CLI."""
    worker_args = WorkerArgs(
        broker="auth.bootstrap.worker.application:worker_factory",
        modules=["auth.infrastructure.messaging.outbox"],
        tasks_pattern=("process_outbox.py",),
        workers=1,
    )
    container = cli_worker_container(worker_args)
    setup_dishka(container, context, finalize_container=True)


main.command(start_worker)

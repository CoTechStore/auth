from dishka.integrations.click import inject
from taskiq.cli.worker.args import WorkerArgs
from taskiq.cli.worker.run import run_worker


@inject
def start_worker(worker_args: WorkerArgs) -> None:
    run_worker(worker_args)

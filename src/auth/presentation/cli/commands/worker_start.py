from taskiq.cli.worker.args import WorkerArgs
from taskiq.cli.worker.run import run_worker


def start_worker() -> None:
    worker_args = WorkerArgs(
        broker="core.entrypoint.worker:worker_factory",
        modules=["core.infrastructure.outbox"],
        tasks_pattern=("process_outbox.py",),
        workers=1,
    )
    run_worker(worker_args)

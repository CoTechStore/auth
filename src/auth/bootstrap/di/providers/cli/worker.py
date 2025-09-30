from dishka import Provider, Scope, from_context
from taskiq.cli.worker.args import WorkerArgs


class CliWorkerConfigProvider(Provider):
    """Провайдер конфигураций для cli-команд."""

    scope = Scope.APP

    worker_args = from_context(WorkerArgs)

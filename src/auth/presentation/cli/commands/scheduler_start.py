from collections.abc import AsyncIterator

from dishka import FromDishka
from dishka.integrations.click import inject
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker

from auth.presentation.cli.wrapper import async_command


@async_command
@inject
async def start_scheduler(
    taskiq_broker: FromDishka[AioPikaBroker],
) -> AsyncIterator[None]:
    scheduler = TaskiqScheduler(
        broker=taskiq_broker,
        sources=[LabelScheduleSource(taskiq_broker)],
    )

    if taskiq_broker.is_worker_process:
        await scheduler.startup()

    yield

    if taskiq_broker.is_worker_process:
        await scheduler.shutdown()

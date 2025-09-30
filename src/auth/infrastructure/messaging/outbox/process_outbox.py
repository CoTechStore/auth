from dishka import FromDishka
from dishka.integrations.taskiq import inject

from auth.infrastructure.messaging.outbox.outbox_processor import OutboxProcessor


@inject
async def process_outbox(processor: FromDishka[OutboxProcessor]) -> None:
    await processor.process()

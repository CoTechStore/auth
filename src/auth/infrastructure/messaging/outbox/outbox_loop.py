import asyncio
import signal
from dataclasses import dataclass, field
from typing import cast

from structlog.stdlib import BoundLogger
from taskiq import AsyncTaskiqDecoratedTask, SendTaskError
from taskiq_aio_pika import AioPikaBroker

from auth.application.common.application_error import ApplicationError
from auth.infrastructure.errors import InfrastructureError


@dataclass(slots=True)
class OutboxLoop:
    taskiq_broker: AioPikaBroker
    logger: BoundLogger
    interval: float
    stop_event: asyncio.Event = field(default_factory=asyncio.Event)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def start(self) -> None:
        """Start an infinite loop of processing outbox."""
        await self.logger.ainfo(
            f"Start {self.__class__.__name__}, for background processing "
            f"with a {self.interval} second interval."
        )

        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda _: self.stop_event.set(), ())

        await asyncio.sleep(8.0)
        process_outbox = cast(
            AsyncTaskiqDecoratedTask, self.taskiq_broker.find_task("process_outbox")
        )

        while not self.stop_event.is_set():
            start_time = loop.time()
            async with self.lock:
                try:
                    await process_outbox.kiq()
                except (ApplicationError, InfrastructureError, SendTaskError):
                    await self.logger.awarning(
                        "Error during process outbox in event loop."
                    )
            elapsed = loop.time() - start_time
            await asyncio.sleep(max(0.0, self.interval - elapsed))

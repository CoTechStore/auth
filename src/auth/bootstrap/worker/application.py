import asyncio
from typing import cast

from dishka.integrations.taskiq import setup_dishka
from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitQueue
from faststream.security import SASLPlaintext
from structlog.stdlib import BoundLogger
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

from auth.bootstrap.config import get_config
from auth.bootstrap.di.containers.worker import worker_container
from auth.infrastructure.logging import get_logger_config
from auth.infrastructure.messaging.config import (
    RabbitConfig,
    QueueName,
    RoutingKeyName,
    ExchangeName,
)
from auth.infrastructure.messaging.outbox.outbox_loop import OutboxLoop
from auth.infrastructure.messaging.outbox.process_outbox import process_outbox


def setup_faststream_broker(rabbit_config: RabbitConfig) -> RabbitBroker:
    security = SASLPlaintext(
        username=rabbit_config.user,
        password=rabbit_config.password,
    )
    return RabbitBroker(
        host=rabbit_config.host,
        port=rabbit_config.port,
        security=security,
        timeout=rabbit_config.timeout,
    )


def setup_taskiq_broker(
    rabbit_config: RabbitConfig, faststream_broker: RabbitBroker
) -> AioPikaBroker:
    taskiq_broker = AioPikaBroker(
        url=rabbit_config.uri, taskiq_return_missed_task=True, prefetch_count=1
    )
    taskiq_broker.state.faststream_broker = faststream_broker
    return taskiq_broker


def setup_logger(taskiq_broker: AioPikaBroker, logger: BoundLogger) -> None:
    taskiq_broker.state.logger = logger


def setup_outbox_loop(taskiq_broker: AioPikaBroker, interval_task: float) -> None:
    logger = cast("BoundLogger", taskiq_broker.state.logger)
    taskiq_broker.state.outbox_loop = OutboxLoop(taskiq_broker, logger, interval_task)


def setup_tasks_to_taskiq(taskiq_broker: AioPikaBroker) -> None:
    taskiq_broker.register_task(process_outbox, task_name="process_outbox")


async def start_broker(taskiq_state: TaskiqState) -> None:
    faststream_broker = cast("RabbitBroker", taskiq_state.faststream_broker)
    await faststream_broker.start()


async def bind_queue_to_exchange(taskiq_state: TaskiqState) -> None:
    faststream_broker = cast("RabbitBroker", taskiq_state.faststream_broker)

    auth_exchange = await faststream_broker.declare_exchange(
        RabbitExchange(name=ExchangeName.AUTH, durable=True, type=ExchangeType.TOPIC)
    )
    auth_queue = await faststream_broker.declare_queue(
        RabbitQueue(name=QueueName.AUTH, durable=True)
    )

    await auth_queue.bind(exchange=auth_exchange, routing_key=RoutingKeyName.USER)


async def start_outbox_loop(taskiq_state: TaskiqState) -> None:
    outbox_loop = cast("OutboxLoop", taskiq_state.outbox_loop)
    loop = asyncio.get_running_loop()

    _ = loop.create_task(outbox_loop.start())  # noqa: RUF006


async def stop_broker(taskiq_state: TaskiqState) -> None:
    faststream_broker = cast("RabbitBroker", taskiq_state.faststream_broker)
    await faststream_broker.stop()


def setup_event_handlers(taskiq_broker: AioPikaBroker) -> None:
    taskiq_broker.add_event_handler(TaskiqEvents.WORKER_STARTUP, start_broker)
    taskiq_broker.add_event_handler(TaskiqEvents.WORKER_STARTUP, bind_queue_to_exchange)
    taskiq_broker.add_event_handler(TaskiqEvents.WORKER_STARTUP, start_outbox_loop)
    taskiq_broker.add_event_handler(TaskiqEvents.WORKER_SHUTDOWN, stop_broker)


def worker_factory() -> AioPikaBroker:
    """Worker application entrypoint."""
    config = get_config()
    logger_config = get_logger_config(config.app_config)
    interval_task = config.rabbit_config.interval

    faststream_broker = setup_faststream_broker(config.rabbit_config)
    taskiq_broker = setup_taskiq_broker(config.rabbit_config, faststream_broker)
    container = worker_container(
        faststream_broker, config.rabbit_config, config.postgres_config, logger_config
    )
    setup_logger(taskiq_broker, logger_config)
    setup_outbox_loop(taskiq_broker, interval_task)
    setup_tasks_to_taskiq(taskiq_broker)
    setup_event_handlers(taskiq_broker)
    setup_dishka(container=container, broker=taskiq_broker)
    return taskiq_broker

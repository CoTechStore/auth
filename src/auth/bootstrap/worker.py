from typing import cast

from dishka.integrations.taskiq import setup_dishka
from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

from auth.bootstrap.config import get_config
from auth.bootstrap.di.containers.worker import worker_container
from auth.infrastructure.logging import get_logger_config
from auth.infrastructure.outbox.config import RabbitConfig
from auth.infrastructure.outbox.outbox_publisher import ExchangeName
from auth.infrastructure.outbox.process_outbox import process_outbox


def setup_faststream_broker(rabbit_config: RabbitConfig) -> RabbitBroker:
    return RabbitBroker(rabbit_config.uri)


def setup_taskiq_broker(
    rabbit_config: RabbitConfig, faststream_broker: RabbitBroker
) -> AioPikaBroker:
    taskiq_broker = AioPikaBroker(
        url=rabbit_config.uri, taskiq_return_missed_task=True, prefetch_count=1
    )
    taskiq_broker.state.faststream_broker = faststream_broker
    return taskiq_broker


def setup_tasks_to_taskiq(taskiq_broker: AioPikaBroker) -> None:
    taskiq_broker.register_task(
        process_outbox, task_name="process_outbox", schedule=[{"cron": "*/3 * * * * *"}]
    )


async def start_broker(taskiq_state: TaskiqState) -> None:
    faststream_broker = cast("RabbitBroker", taskiq_state.faststream_broker)
    await faststream_broker.start()


async def bind_queue_to_exchange(taskiq_state: TaskiqState) -> None:
    faststream_broker = cast("RabbitBroker", taskiq_state.faststream_broker)
    await faststream_broker.declare_exchange(
        RabbitExchange(name=ExchangeName.AUTH, durable=True, type=ExchangeType.DIRECT)
    )


def setup_event_handlers(taskiq_broker: AioPikaBroker) -> None:
    taskiq_broker.add_event_handler(TaskiqEvents.WORKER_STARTUP, start_broker)
    taskiq_broker.add_event_handler(TaskiqEvents.WORKER_STARTUP, bind_queue_to_exchange)


def worker_factory() -> AioPikaBroker:
    config = get_config()
    logger_config = get_logger_config(config.app_config)
    faststream_broker = setup_faststream_broker(config.rabbit_config)
    taskiq_broker = setup_taskiq_broker(config.rabbit_config, faststream_broker)
    container = worker_container(
        faststream_broker, config.rabbit_config, config.postgres_config, logger_config
    )
    setup_tasks_to_taskiq(taskiq_broker)
    setup_event_handlers(taskiq_broker)
    setup_dishka(container=container, broker=taskiq_broker)
    return taskiq_broker

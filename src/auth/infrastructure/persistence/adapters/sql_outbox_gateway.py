from dataclasses import asdict

from sqlalchemy import Row, and_, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.infrastructure.outbox.interfaces import OutboxGateway
from auth.infrastructure.outbox.outbox_message import OutboxMessage
from auth.infrastructure.persistence.sqlalchemy.tables import OUTBOX_TABLE


class SqlOutboxGatewayImpl(OutboxGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, message: OutboxMessage) -> None:
        stmt = insert(OUTBOX_TABLE).values(asdict(message))
        await self.__session.execute(stmt)

    async def delete(self, message: OutboxMessage) -> None:
        stmt = delete(OUTBOX_TABLE).where(
            and_(OUTBOX_TABLE.c.message_id == message.message_id)
        )
        await self.__session.execute(stmt)

    async def select(self) -> list[OutboxMessage]:
        stmt = select(OUTBOX_TABLE)
        result = (await self.__session.execute(stmt)).fetchall()
        return [self.__load(message) for message in result]

    @staticmethod
    def __load(message_row: Row) -> OutboxMessage:
        return OutboxMessage(
            message_id=message_row.message_id,
            event_type=message_row.event_type,
            data=message_row.data,
        )

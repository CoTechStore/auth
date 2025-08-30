from sqlalchemy import UUID, Column, DateTime, ForeignKey, Table

from auth.domain.session.session import Session
from auth.infrastructure.persistence.sqlalchemy.tables.base import MAPPER_REGISTRY

SESSIONS_TABLE = Table(
    "sessions",
    MAPPER_REGISTRY.metadata,
    Column("session_id", UUID, primary_key=True),
    Column("user_id", UUID, ForeignKey("users.user_id")),
    Column("expires_at", DateTime(timezone=True), nullable=False),
    Column("iat", DateTime(timezone=True), nullable=False),
)


def map_sessions_table() -> None:
    """Императивный маппинг таблицы sessions."""
    MAPPER_REGISTRY.map_imperatively(
        Session,
        SESSIONS_TABLE,
        properties={
            "_entity_id": SESSIONS_TABLE.c.session_id,
            "_user_id": SESSIONS_TABLE.c.user_id,
            "_expires_at": SESSIONS_TABLE.c.expires_at,
            "_iat": SESSIONS_TABLE.c.iat,
        },
    )

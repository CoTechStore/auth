from sqlalchemy import UUID, Column, String, Table

from auth.infrastructure.persistence.sqlalchemy.tables.base import MAPPER_REGISTRY

OUTBOX_TABLE = Table(
    "outbox",
    MAPPER_REGISTRY.metadata,
    Column("outbox_id", UUID, primary_key=True),
    Column("event_type", String(length=100), nullable=False),
    Column("data", String, nullable=False),
)

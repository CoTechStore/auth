from sqlalchemy import UUID, Boolean, Column, LargeBinary, String, Table
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import composite

from auth.domain.user.user import User
from auth.domain.user.value_objects import Username
from auth.infrastructure.persistence.sqlalchemy.tables.base import MAPPER_REGISTRY

USERS_TABLE = Table(
    "users",
    MAPPER_REGISTRY.metadata,
    Column("user_id", UUID, primary_key=True),
    Column("username", String(length=100), unique=True, nullable=False),
    Column("hash_password", LargeBinary, nullable=False),
    Column("is_active", Boolean, nullable=False),
    Column(
        "user_type",
        ENUM("default-user", "super-user", name="user_type"),
        nullable=False,
    ),
)


def map_users_table() -> None:
    """Императивный маппинг таблицы users."""
    MAPPER_REGISTRY.map_imperatively(
        User,
        USERS_TABLE,
        properties={
            "_entity_id": USERS_TABLE.c.user_id,
            "_username": composite(Username, USERS_TABLE.c.username),
            "_hash_password": USERS_TABLE.c.hash_password,
            "_is_active": USERS_TABLE.c.is_active,
            "_user_type": USERS_TABLE.c.user_type,
        },
    )

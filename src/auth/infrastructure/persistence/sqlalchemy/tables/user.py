from sqlalchemy import UUID, Boolean, Column, Index, LargeBinary, String, Table
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import composite

from auth.domain.user.role_enum import AdminRoleEnum, StaffRoleEnum
from auth.domain.user.user import User
from auth.domain.user.value_objects import Login, Role
from auth.infrastructure.persistence.sqlalchemy.tables.base import MAPPER_REGISTRY

USERS_TABLE = Table(
    "users",
    MAPPER_REGISTRY.metadata,
    Column("user_id", UUID, primary_key=True),
    Column("login", String(length=100), unique=True, nullable=False),
    Column("hash_password", LargeBinary, nullable=False),
    Column("hidden", Boolean, default=False, nullable=False),
    Column("extended", Boolean, default=False, nullable=False),
    Column("organization_name", String(length=300), nullable=True, default=None),
    Column(
        "role",
        ENUM(*AdminRoleEnum.list(), *StaffRoleEnum.list(), name="user_role_enum"),
        nullable=False,
    ),
    Index(
        "unique_admin",
        "role",
        unique=True,
        postgresql_where="role = 'admin'",
    ),
)


def map_users_table() -> None:
    """Императивный маппинг таблицы users."""
    MAPPER_REGISTRY.map_imperatively(
        User,
        USERS_TABLE,
        properties={
            "_entity_id": USERS_TABLE.c.user_id,
            "_login": composite(Login, USERS_TABLE.c.login),
            "_hash_password": USERS_TABLE.c.hash_password,
            "_hidden": USERS_TABLE.c.hidden,
            "_role": composite(Role, USERS_TABLE.c.role, USERS_TABLE.c.extended),
            "_organization_name": USERS_TABLE.c.organization_name,
        },
    )

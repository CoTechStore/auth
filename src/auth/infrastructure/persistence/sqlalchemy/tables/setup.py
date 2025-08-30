from auth.infrastructure.persistence.sqlalchemy.tables import (
    map_sessions_table,
    map_users_table,
)


def setup_mappings() -> None:
    map_users_table()
    map_sessions_table()

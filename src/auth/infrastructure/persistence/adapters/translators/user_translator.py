from collections.abc import Callable, Generator
from typing import Any, ClassVar

from sqlalchemy import ColumnElement, and_, exists, select

from auth.domain.user.specifications import UserSpecifications
from auth.infrastructure.persistence.sqlalchemy.tables import (
    SESSIONS_TABLE,
    USERS_TABLE,
)


class UserTranslator:
    __CONDITION_MAP: ClassVar[dict[str, Callable[[Any], ColumnElement[bool]]]] = {
        "user_id": lambda value: USERS_TABLE.c.user_id == value,
        "exists_session_id": lambda value: exists(
            select(1).where(
                and_(
                    SESSIONS_TABLE.c.user_id == USERS_TABLE.c.user_id,
                    SESSIONS_TABLE.c.session_id == value,
                )
            )
        ),
    }

    def __init__(self, specifications: UserSpecifications) -> None:
        self.__specifications = specifications

    def specifications_mapping(self) -> Generator[ColumnElement[bool], Any, None]:
        conditions = (
            self.__CONDITION_MAP[name_specification](value)
            for name_specification, value in self.__specifications.items()
        )
        return conditions

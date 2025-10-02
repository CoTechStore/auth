from datetime import UTC, datetime

from auth.application.ports import TimeProvider
from auth.bootstrap.config import AuthConfig


class TimeProviderImpl(TimeProvider):
    """Класс реализующий работу с временем."""

    def __init__(self, auth_config: AuthConfig) -> None:
        self.__auth_config = auth_config

    def current_time(self) -> datetime:
        return datetime.now(UTC)

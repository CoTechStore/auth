from datetime import UTC, datetime

from auth.application.ports import TimeProvider
from auth.bootstrap.config import AuthConfig


class TimeProviderImpl(TimeProvider):
    """Класс реализующий работу с временем."""

    def __init__(self, auth_config: AuthConfig) -> None:
        self.__auth_config = auth_config

    def current_time(self) -> datetime:
        return datetime.now(UTC)

    def unix_time(self, current_time: datetime) -> int:
        return int(
            (
                current_time.astimezone(UTC) - datetime(1970, 1, 1, tzinfo=UTC)
            ).total_seconds()
            * 1000
        )

    def access_token_expires(self, current_time: datetime) -> datetime:
        expires_time = current_time + self.__auth_config.access_token_expires_minutes
        return expires_time

    def refresh_token_expires(self, current_time: datetime) -> datetime:
        expires_time = current_time + self.__auth_config.refresh_token_expires_minutes
        return expires_time

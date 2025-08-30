from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from auth.domain.session.session import Session
from auth.domain.user.user import User


class TokenProvider(ABC):
    @abstractmethod
    def create_access_token(
        self, user: User, session: Session, expires: datetime
    ) -> str: ...

    @abstractmethod
    def create_refresh_token(
        self, user: User, session: Session, expires: datetime
    ) -> str: ...

    @abstractmethod
    def decode_token_verify(self, token: str) -> dict[str, Any] | None: ...

    @abstractmethod
    def decode_token_not_verify(self, token: str) -> dict[str, Any]: ...

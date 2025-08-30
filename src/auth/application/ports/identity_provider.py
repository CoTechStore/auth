from abc import ABC, abstractmethod

from auth.domain.session.session_id import SessionId
from auth.domain.user.value_objects.user_id import UserId


class IdentityProvider(ABC):
    @abstractmethod
    def current_user_id(self) -> UserId | None: ...

    @abstractmethod
    def current_session_id(self) -> SessionId | None: ...

from typing import Final
from uuid import UUID

from starlette.requests import Request

from auth.application.ports.identity_provider import IdentityProvider
from auth.domain.session.session_id import SessionId
from auth.domain.user.value_objects.user_id import UserId


class IdentityProviderImpl(IdentityProvider):
    __USER_ID_HEADER: Final[str] = "X-User-ID"
    __SESSION_ID_HEADER: Final[str] = "X-Session-ID"

    def __init__(self, request: Request) -> None:
        self.__request = request

    def current_user_id(self) -> UserId | None:
        user_id = self.__request.headers.get(self.__USER_ID_HEADER)

        if not user_id:
            return None

        try:
            return UserId(UUID(user_id))
        except ValueError:
            return None

    def current_session_id(self) -> SessionId | None:
        session_id = self.__request.headers.get(self.__SESSION_ID_HEADER)

        if not session_id:
            return None

        try:
            return SessionId(UUID(session_id))
        except ValueError:
            return None

from dataclasses import dataclass

from auth.application.common.application_error import AppErrorType, ApplicationError
from auth.application.common.const import errors as text
from auth.application.common.handlers import CommandHandler
from auth.application.common.markers import Command
from auth.application.ports import IdentityProvider, PasswordVerify, TimeProvider
from auth.domain.session.factory import SessionFactory
from auth.domain.session.repository import SessionRepository
from auth.domain.user.repository import UserRepository


@dataclass(frozen=True, slots=True)
class LogoutCommand(Command[None]): ...


class LogoutHandler(CommandHandler[LogoutCommand, None]):
    def __init__(
        self,
        identity_provider: IdentityProvider,
        user_repository: UserRepository,
        password_verify: PasswordVerify,
        session_factory: SessionFactory,
        time_provider: TimeProvider,
        session_repository: SessionRepository,
    ) -> None:
        self.__identity_provider = identity_provider
        self.__user_repository = user_repository
        self.__password_verify = password_verify
        self.__session_factory = session_factory
        self.__time_provider = time_provider
        self.__session_repository = session_repository

    async def handle(self, command: LogoutCommand) -> None:
        session_id = self.__identity_provider.current_session_id()

        if not session_id:
            raise ApplicationError(
                type=AppErrorType.UNAUTHENTICATED, message=text.UNAUTHENTICATED
            )

        session = await self.__session_repository.with_session_id(session_id)

        if not session:
            raise ApplicationError(
                type=AppErrorType.UNAUTHENTICATED, message=text.UNAUTHENTICATED
            )

        await self.__session_repository.delete(session)

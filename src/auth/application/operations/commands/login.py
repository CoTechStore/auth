from dataclasses import dataclass
from datetime import datetime

from auth.application.common.application_error import AppErrorType, ApplicationError
from auth.application.common.const import errors as text
from auth.application.common.handlers import CommandHandler
from auth.application.common.markers import Command
from auth.application.ports import IdentityProvider, PasswordVerify
from auth.domain.session.factory import SessionFactory
from auth.domain.session.repository import SessionRepository
from auth.domain.session.session_id import SessionId
from auth.domain.user.repository import UserRepository
from auth.domain.user.value_objects import Username, Password, UserId


@dataclass(frozen=True, slots=True)
class LoginResponse:
    user_id: UserId
    session_id: SessionId
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class LoginCommand(Command[LoginResponse]):
    username: str
    password: str


class LoginHandler(CommandHandler[LoginCommand, LoginResponse]):
    def __init__(
        self,
        identity_provider: IdentityProvider,
        user_repository: UserRepository,
        password_verify: PasswordVerify,
        session_factory: SessionFactory,
        session_repository: SessionRepository,
    ) -> None:
        self.__identity_provider = identity_provider
        self.__user_repository = user_repository
        self.__password_verify = password_verify
        self.__session_factory = session_factory
        self.__session_repository = session_repository

    async def handle(self, command: LoginCommand) -> LoginResponse:
        user_id = self.__identity_provider.current_user_id()

        if user_id:
            raise ApplicationError(
                type=AppErrorType.UNAUTHENTICATED,
                message=text.USER_ALREADY_AUTHENTICATED,
            )

        username_vo = Username(command.username)
        password_vo = Password(command.password)

        user = await self.__user_repository.with_username(username_vo.value)

        if not user:
            raise ApplicationError(
                type=AppErrorType.UNAUTHENTICATED, message=text.INVALID_LOGIN_OR_PASSWORD
            )

        if not self.__password_verify.verify(password_vo.value, user.hash_password):
            raise ApplicationError(
                type=AppErrorType.UNAUTHENTICATED, message=text.INVALID_LOGIN_OR_PASSWORD
            )

        session = self.__session_factory.authenticate_user(user.entity_id)

        self.__session_repository.add(session)

        return LoginResponse(
            user_id=user.entity_id,
            session_id=session.entity_id,
            expires_at=session.expires_at,
        )

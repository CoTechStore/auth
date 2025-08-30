from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from auth.application.common.application_error import AppErrorType, ApplicationError
from auth.application.common.const import errors as text
from auth.application.common.dto.user_info_dto import UserInfoDto
from auth.application.common.handlers import CommandHandler
from auth.application.common.markers import Command
from auth.application.ports import IdentityProvider, PasswordVerify, TimeProvider
from auth.application.ports.token_provider import TokenProvider
from auth.domain.session.factory import SessionFactory
from auth.domain.session.repository import SessionRepository
from auth.domain.user.repository import UserRepository
from auth.domain.user.value_objects import Login, Password

if TYPE_CHECKING:
    from auth.domain.user.user import User


@dataclass(frozen=True, slots=True)
class LoginResponse:
    access_token: str
    refresh_token: str
    expires: int
    user_info: UserInfoDto


@dataclass(frozen=True, slots=True)
class LoginCommand(Command[LoginResponse]):
    login: str
    password: str


class LoginHandler(CommandHandler[LoginCommand, LoginResponse]):
    def __init__(
        self,
        identity_provider: IdentityProvider,
        user_repository: UserRepository,
        password_verify: PasswordVerify,
        session_factory: SessionFactory,
        token_provider: TokenProvider,
        time_provider: TimeProvider,
        session_repository: SessionRepository,
    ) -> None:
        self.__identity_provider = identity_provider
        self.__user_repository = user_repository
        self.__password_verify = password_verify
        self.__session_factory = session_factory
        self.__token_provider = token_provider
        self.__time_provider = time_provider
        self.__session_repository = session_repository

    async def handle(self, command: LoginCommand) -> LoginResponse:
        user_id = self.__identity_provider.current_user_id()

        if user_id:
            raise ApplicationError(
                type=AppErrorType.UNAUTHENTICATED,
                message=text.USER_ALREADY_AUTHENTICATED,
            )

        login_vo = Login(command.login)
        password_vo = Password(command.password)

        user = cast("User", await self.__user_repository.with_login(login_vo.value))

        if not self.__password_verify.verify(password_vo.value, user.hash_password):
            raise ApplicationError(
                type=AppErrorType.UNAUTHORIZED, message=text.INVALID_LOGIN_OR_PASSWORD
            )

        current_time = self.__time_provider.current_time()
        access_expires = self.__time_provider.access_token_expires(current_time)
        refresh_expires = self.__time_provider.refresh_token_expires(current_time)
        access_unix_expires = self.__time_provider.unix_time(access_expires)

        session = await self.__session_factory.authenticate_user(
            user.entity_id, iat=current_time, expires=refresh_expires
        )

        access_token = self.__token_provider.create_access_token(
            user, session, access_expires
        )
        refresh_token = self.__token_provider.create_refresh_token(
            user, session, refresh_expires
        )

        self.__session_repository.add(session)

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires=access_unix_expires,
            user_info=UserInfoDto(
                id=user.entity_id,
                login=user.login_vo.value,
                role=user.role_name,
                extended=user.role_extended,
                hidden=user.hidden,
                organization_name=user.organization_name,
            ),
        )

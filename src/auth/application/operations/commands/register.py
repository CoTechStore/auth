from dataclasses import dataclass

from auth.application.common.application_error import AppErrorType, ApplicationError
from auth.application.common.const import errors as text
from auth.application.common.handlers import CommandHandler
from auth.application.common.markers import Command
from auth.application.ports import PasswordVerify, IdentityProvider
from auth.domain.user.factory import UserFactory
from auth.domain.user.repository import UserRepository
from auth.domain.user.value_objects import Username, Password, UserId


@dataclass(frozen=True, slots=True)
class RegisterCommand(Command[UserId]):
    username: str
    password: str


class RegisterHandler(CommandHandler[RegisterCommand, UserId]):
    def __init__(
        self,
        identity_provider: IdentityProvider,
        user_factory: UserFactory,
        user_repository: UserRepository,
        password_verify: PasswordVerify,
    ) -> None:
        self.__identity_provider = identity_provider
        self.__user_factory = user_factory
        self.__user_repository = user_repository
        self.__password_verify = password_verify

    async def handle(self, command: RegisterCommand) -> UserId:
        user_id = self.__identity_provider.current_user_id()

        if user_id:
            raise ApplicationError(
                type=AppErrorType.UNAUTHENTICATED, message=text.USER_ALREADY_AUTHENTICATED
            )

        username_vo = Username(command.username)
        password_vo = Password(command.password)

        if await self.__user_repository.with_username(username_vo.value):
            raise ApplicationError(
                type=AppErrorType.CONFLICT, message=text.USER_ALREADY_EXISTS
            )

        user = await self.__user_factory.create_user(
            username=username_vo, password=password_vo
        )

        self.__user_repository.add(user)

        return user.entity_id

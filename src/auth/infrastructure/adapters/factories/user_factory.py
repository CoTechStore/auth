from auth.domain.shared.domain_event import DomainEventAdder
from auth.domain.user.factory import UserFactory
from auth.domain.user.user import User
from auth.domain.user.value_objects import Login, Role, UserId


class UserFactoryImpl(UserFactory):
    def __init__(
        self,
        event_adder: DomainEventAdder,
    ) -> None:
        self.__event_adder = event_adder

    async def create_user(
        self,
        user_id: UserId,
        login: Login,
        hash_password: bytes,
        hidden: bool,
        role: Role,
        organization_name: str | None,
    ) -> User:
        user = User(
            user_id=user_id,
            event_adder=self.__event_adder,
            login=login,
            hash_password=hash_password,
            hidden=hidden,
            role=role,
            organization_name=organization_name,
        )

        return user

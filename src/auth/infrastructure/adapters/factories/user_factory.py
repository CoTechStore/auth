from auth.application.ports import IdGenerator, PasswordHasher
from auth.domain.shared.domain_event import DomainEventAdder
from auth.domain.user.events import UserCreated
from auth.domain.user.factory import UserFactory
from auth.domain.user.user import User
from auth.domain.user.value_objects import Username, Password


class UserFactoryImpl(UserFactory):
    def __init__(
        self,
        id_generator: IdGenerator,
        event_adder: DomainEventAdder,
        password_hasher: PasswordHasher,
    ) -> None:
        self.__id_generator = id_generator
        self.__event_adder = event_adder
        self.__password_hasher = password_hasher

    async def create_user(self, username: Username, password: Password) -> User:
        user_id = self.__id_generator.generate_user_id()

        user = User(
            user_id=user_id,
            event_adder=self.__event_adder,
            username=username,
            hash_password=self.__password_hasher.hash(password.value),
        )

        user.track_event(event=UserCreated(user_id=user_id))

        return user

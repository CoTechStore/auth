from auth.application.ports import IdGenerator, TimeProvider
from auth.domain.session.factory import SessionFactory
from auth.domain.session.session import Session
from auth.domain.shared.domain_event import DomainEventAdder
from auth.domain.user.value_objects import UserId


class SessionFactoryImpl(SessionFactory):
    def __init__(
        self,
        id_generator: IdGenerator,
        time_provider: TimeProvider,
        event_adder: DomainEventAdder,
    ) -> None:
        self.__id_generator = id_generator
        self.__time_provider = time_provider
        self.__event_adder = event_adder

    def authenticate_user(self, user_id: UserId) -> Session:
        current_time = self.__time_provider.current_time()
        session = Session(
            session_id=self.__id_generator.generate_session_id(),
            event_adder=self.__event_adder,
            user_id=user_id,
            iat=current_time,
            expires_at=current_time,
        )

        return session

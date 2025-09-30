from abc import ABC, abstractmethod

from auth.domain.session.session import Session
from auth.domain.user.value_objects import UserId


class SessionFactory(ABC):
    @abstractmethod
    def authenticate_user(self, user_id: UserId) -> Session: ...

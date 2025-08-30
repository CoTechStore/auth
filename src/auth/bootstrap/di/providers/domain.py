from dishka import Provider, Scope, provide

from auth.domain.session.factory import SessionFactory
from auth.domain.session.repository import SessionRepository
from auth.domain.user.factory import UserFactory
from auth.domain.user.repository import UserRepository
from auth.infrastructure.adapters.factories import SessionFactoryImpl, UserFactoryImpl
from auth.infrastructure.persistence.adapters import (
    SqlSessionRepositoryImpl,
    SqlUserRepositoryImpl,
)


class WebDomainAdaptersProvider(Provider):
    """Провайдер адаптеров домена."""

    scope = Scope.REQUEST

    user_factory = provide(UserFactoryImpl, provides=UserFactory)
    user_repository = provide(SqlUserRepositoryImpl, provides=UserRepository)

    session_factory = provide(SessionFactoryImpl, provides=SessionFactory)
    session_repository = provide(SqlSessionRepositoryImpl, provides=SessionRepository)

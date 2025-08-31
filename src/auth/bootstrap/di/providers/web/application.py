from dishka import AnyOf, Provider, Scope, alias, provide
from sqlalchemy.ext.asyncio import AsyncSession
from structlog.stdlib import BoundLogger

from auth.application.ports import (
    DomainEventsRaiser,
    IdGenerator,
    Logger,
    PasswordVerify,
    TimeProvider,
    TransactionManager,
)
from auth.domain.shared.domain_event import DomainEventAdder
from auth.infrastructure.adapters import (
    BcryptPasswordImpl,
    DomainEventsImpl,
    IdGeneratorImpl,
    TimeProviderImpl,
)


class ApplicationAdaptersProvider(Provider):
    """Провайдер адаптеров приложения."""

    scope = Scope.REQUEST

    domain_events = provide(
        DomainEventsImpl, provides=AnyOf[DomainEventAdder, DomainEventsRaiser]
    )
    bcrypt_password = provide(BcryptPasswordImpl, provides=PasswordVerify)

    id_generator = provide(IdGeneratorImpl, provides=IdGenerator, scope=Scope.APP)
    time_provider = provide(TimeProviderImpl, provides=TimeProvider, scope=Scope.APP)

    transaction = alias(AsyncSession, provides=TransactionManager)
    logger = alias(BoundLogger, provides=Logger)

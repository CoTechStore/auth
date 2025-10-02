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
    PasswordHasher,
)
from auth.domain.shared.domain_event import DomainEventAdder
from auth.infrastructure.adapters import (
    BcryptPasswordImpl,
    DomainEventsImpl,
    IdGeneratorImpl,
    TimeProviderImpl,
)
from auth.infrastructure.messaging.outbox.interfaces import OutboxGateway
from auth.infrastructure.messaging.outbox.sql_outbox_gateway import SqlOutboxGatewayImpl


class ApplicationAdaptersProvider(Provider):
    """Провайдер адаптеров приложения."""

    scope = Scope.REQUEST

    domain_events = provide(
        DomainEventsImpl, provides=AnyOf[DomainEventAdder, DomainEventsRaiser]
    )
    bcrypt_password = provide(
        BcryptPasswordImpl, provides=AnyOf[PasswordHasher, PasswordVerify]
    )
    outbox_gateway = provide(SqlOutboxGatewayImpl, provides=OutboxGateway)
    id_generator = provide(IdGeneratorImpl, provides=IdGenerator, scope=Scope.APP)
    time_provider = provide(TimeProviderImpl, provides=TimeProvider, scope=Scope.APP)

    transaction = alias(AsyncSession, provides=TransactionManager)
    logger = alias(BoundLogger, provides=Logger)

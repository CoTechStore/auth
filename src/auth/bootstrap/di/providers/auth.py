from dishka import Provider, Scope, provide

from auth.application.ports import IdentityProvider
from auth.presentation.web.identity_provider import IdentityProviderImpl


class AuthProvider(Provider):
    """Провайдер адаптеров приложения."""

    scope = Scope.REQUEST

    identity_provider = provide(IdentityProviderImpl, provides=IdentityProvider)

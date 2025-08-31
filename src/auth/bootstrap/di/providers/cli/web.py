from alembic.config import Config as AlembicConfig
from dishka import Provider, Scope, from_context
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer


class CliWebConfigProvider(Provider):
    """Провайдер конфигураций для cli-команд."""

    scope = Scope.APP

    alembic_config = from_context(AlembicConfig)
    uvicorn_config = from_context(UvicornConfig)
    uvicorn_server = from_context(UvicornServer)

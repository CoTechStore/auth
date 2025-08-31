from alembic.config import Config as AlembicConfig
from dishka import Container, make_container
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from auth.bootstrap.di.providers.cli import CliWebConfigProvider


def cli_web_container(
    alembic_config: AlembicConfig,
    uvicorn_config: UvicornConfig,
    uvicorn_server: UvicornServer,
) -> Container:
    """Создание контейнера для CLI."""
    return make_container(
        CliWebConfigProvider(),
        context={
            UvicornConfig: uvicorn_config,
            UvicornServer: uvicorn_server,
            AlembicConfig: alembic_config,
        },
    )

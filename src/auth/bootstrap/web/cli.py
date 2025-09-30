from click import Context, group, pass_context
from dishka.integrations.click import setup_dishka
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from auth.bootstrap.config import get_config
from auth.bootstrap.di.containers.cli.web import cli_web_container
from auth.infrastructure.persistence.alembic.config import get_alembic_config
from auth.presentation.cli.commands.migrations import (
    make_migrations,
    migrate,
    rollback,
    show_current_migration,
)
from auth.presentation.cli.commands.server_start import start_uvicorn


@group()
@pass_context
def main(context: Context) -> None:
    """Старт приложением через CLI."""
    app_config = get_config().app_config
    alembic_config = get_alembic_config()
    uvicorn_config = UvicornConfig(
        app="auth.bootstrap.web:app_factory",
        host=app_config.server_host,
        port=app_config.server_port,
        factory=True,
    )
    uvicorn_server = UvicornServer(uvicorn_config)
    container = cli_web_container(alembic_config, uvicorn_config, uvicorn_server)
    setup_dishka(container, context, finalize_container=True)


main.command(start_uvicorn)
main.command(make_migrations)
main.command(migrate)
main.command(rollback)
main.command(show_current_migration)

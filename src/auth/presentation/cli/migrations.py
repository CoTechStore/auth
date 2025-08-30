from alembic.command import current as alembic_current
from alembic.command import downgrade as alembic_downgrade
from alembic.command import revision as alembic_revision
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from click import argument, option
from dishka import FromDishka as Depends
from dishka.integrations.click import inject


@option("--message", "-m", required=True, help="Сообщение миграции.")
@inject
def make_migrations(message: str, *, alembic_config: Depends[AlembicConfig]) -> None:
    """
    Создание миграции
    Команда: core make-migrations -m 'message'.
    """
    alembic_revision(alembic_config, message=message, autogenerate=True)


@option("--revision", "-r", default="head", help="Выполнить миграцию.")
@argument("revision", default="head")
@inject
def migrate(revision: str, *, alembic_config: Depends[AlembicConfig]) -> None:
    """
    Выполнение миграции
    Команда: core migrate -r 'message'.
    """
    alembic_upgrade(alembic_config, revision)


@option("--revision", "-r", default="-1", help="Выполнить откат миграции.")
@argument("revision", default="-1")
@inject
def rollback(revision: str, *, alembic_config: Depends[AlembicConfig]) -> None:
    """
    Откат миграции
    Команда: core rollback.
    """
    alembic_downgrade(alembic_config, revision)


@inject
def show_current_migration(alembic_config: Depends[AlembicConfig]) -> None:
    """
    Показать текущую миграцию
    Команда: core show-current-migration.
    """
    alembic_current(alembic_config)

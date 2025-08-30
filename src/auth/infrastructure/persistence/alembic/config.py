from functools import lru_cache
from importlib.resources import files

from alembic.config import Config as AlembicConfig

from auth.bootstrap.config import get_config


@lru_cache
def get_alembic_config() -> AlembicConfig:
    resource = files("auth.infrastructure.persistence.alembic")
    alembic_config = resource.joinpath("alembic.ini")
    config_object = AlembicConfig(str(alembic_config))
    config_object.set_main_option("sqlalchemy.url", get_config().postgres_config.uri)
    return config_object

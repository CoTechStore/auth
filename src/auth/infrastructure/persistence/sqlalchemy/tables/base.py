from sqlalchemy import MetaData
from sqlalchemy.orm import registry

METADATA = MetaData()
MAPPER_REGISTRY = registry(metadata=METADATA)

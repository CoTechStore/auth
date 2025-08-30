import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if is_dataclass(obj) and not isinstance(obj, type):
            return asdict(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)


def to_json(obj: object) -> str:
    return json.dumps(obj, cls=CustomJSONEncoder)

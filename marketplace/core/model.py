from typing import Optional, Any, Callable

import orjson
from pydantic import BaseModel
from pydantic.utils import to_camel


class OrJson:
    @staticmethod
    def loads(obj):
        return orjson.loads(obj)

    @staticmethod
    def dumps(v: Any, default: Optional[Callable[[Any], Any]] = None, option: Optional[int] =None):
        return orjson.dumps(v, default).decode()


class Model(BaseModel):
    class Config:
        json_loads = OrJson.loads
        json_dumps = OrJson.dumps
        frozen = True
        allow_population_by_field_name = True

        @classmethod
        def alias_generator(cls, field: str) -> str:
            return to_camel(field)

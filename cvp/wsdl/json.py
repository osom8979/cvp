# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from json import JSONEncoder
from json import dumps as json_dumps
from typing import Any


def _dumps_default(o: Any) -> Any:
    if isinstance(o, datetime):
        return o.isoformat()
    elif isinstance(o, timedelta):
        return o.total_seconds()
    try:
        return JSONEncoder().default(o)
    except TypeError:
        return str(o)


def dumps(o: Any, indent=4, sort=False) -> str:
    return json_dumps(o, indent=indent, sort_keys=sort, default=_dumps_default)

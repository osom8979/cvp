# -*- coding: utf-8 -*-

from datetime import date, datetime, time, timedelta
from typing import Any

from zeep.xsd.valueobjects import CompoundValue

from cvp.inspect.member import is_private_member

# noinspection PyProtectedMember
from lxml.etree import _Element as _EtreeElement  # isort:skip


def serialize_object(o: Any, target_cls=dict) -> Any:
    if isinstance(o, datetime):
        return o.isoformat()

    if isinstance(o, date):
        return o.isoformat()

    if isinstance(o, time):
        return o.isoformat()

    if isinstance(o, timedelta):
        return o.total_seconds()

    if isinstance(o, _EtreeElement):
        return None

    if isinstance(o, (dict, CompoundValue)):
        result = target_cls()
        for key in o:
            if is_private_member(key):
                continue
            result[key] = serialize_object(o[key], target_cls)
        return result

    if isinstance(o, list):
        return list(serialize_object(sub, target_cls) for sub in o)

    if isinstance(o, (str, int, float, bool, type(None))):
        return o

    raise TypeError(f"Object of type {type(o).__name__} is not serializable")

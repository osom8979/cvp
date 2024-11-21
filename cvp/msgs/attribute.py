# -*- coding: utf-8 -*-

from typing import Final, Optional

MSG_TYPE_ATTR_NAME: Final[str] = "__msg_type__"


def has_msg_type(func) -> bool:
    return hasattr(func, MSG_TYPE_ATTR_NAME)


def get_msg_type(func) -> Optional[int]:
    return getattr(func, MSG_TYPE_ATTR_NAME, None)


def set_msg_type(func, mtype: int) -> None:
    setattr(func, MSG_TYPE_ATTR_NAME, mtype)

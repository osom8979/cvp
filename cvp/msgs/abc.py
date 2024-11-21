# -*- coding: utf-8 -*-

from abc import abstractmethod
from functools import wraps

from cvp.msgs.attribute import set_msg_type
from cvp.msgs.msg_type import MsgType


def abstractmsg(mtype: MsgType):
    def _param_wrapper(func):
        abstractmethod(func)
        set_msg_type(func, mtype)

        @wraps(func)
        def _func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return _func_wrapper

    return _param_wrapper

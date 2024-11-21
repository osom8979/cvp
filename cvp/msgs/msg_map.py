# -*- coding: utf-8 -*-

from inspect import getmembers, isroutine, signature
from typing import Any, Callable, Dict, List, Optional

from cvp.inspect.bind import force_bind
from cvp.msgs.attribute import get_msg_type, has_msg_type
from cvp.msgs.interface import MsgInterface
from cvp.msgs.msg import Msg
from cvp.msgs.msg_type import MsgType, get_msg_type_name


class MsgCallable:
    def __init__(self, func: Callable, same_signature=False):
        self._func = func
        self._same_signature = same_signature

    def __call__(self, *args, **kwargs):
        if self._same_signature:
            return self._func(*args, **kwargs)
        else:
            return force_bind(self._func, *args, **kwargs)()


class MsgWrapper:
    _callbacks: List[MsgCallable]

    def __init__(
        self,
        mtype: MsgType,
        name: str,
        func: Callable[..., Any],
    ):
        self._params = list(signature(func).parameters.keys())
        self._mtype = mtype
        self._name = get_msg_type_name(mtype)
        self._fallback_name = name
        self._fallback_func = func
        self._fallback_signature = signature(func)
        self._callbacks = list()

    def compare_fallback_kwargs(self, func: Callable) -> bool:
        left = [(p.name, p.kind) for p in self._fallback_signature.parameters.values()]
        right = [(p.name, p.kind) for p in signature(func).parameters.values()]
        return left == right

    def __call__(self, msg: Optional[Msg] = None) -> bool:
        kwargs = msg.as_args() if msg else dict()

        for callback in self._callbacks:
            if bool(callback(**kwargs)):
                return True

        return bool(self._fallback_func(**kwargs))

    def append_callback(self, func: Callable) -> None:
        self._callbacks.append(MsgCallable(func, self.compare_fallback_kwargs(func)))

    def clear_callback(self) -> None:
        self._callbacks.clear()


def create_msg_map(obj: Any, cls=MsgInterface) -> Dict[int, MsgWrapper]:
    result = dict()
    msg_interfaces = dict(getmembers(cls))
    msg_attributes = getmembers(obj, lambda a: isroutine(a))

    for key, func in msg_attributes:
        msg_interface = msg_interfaces.get(key)
        if msg_interface is None:
            continue
        if not has_msg_type(msg_interface):
            continue
        msg_type = get_msg_type(msg_interface)
        assert isinstance(msg_type, int)
        result[msg_type] = MsgWrapper(MsgType(msg_type), key, func)

    return result

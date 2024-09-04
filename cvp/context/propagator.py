# -*- coding: utf-8 -*-

from collections import deque
from typing import Deque, Optional

from cvp.context.context import Context
from cvp.patterns.singleton import get_singleton_instance, singleton


class ContextStack:
    _deque: Deque[Context]

    def __init__(self):
        self._deque = deque()

    def get(self) -> Optional[Context]:
        return self._deque[-1] if self._deque else None

    def push(self, context: Context) -> None:
        self._deque.append(context)

    def pop(self) -> Context:
        return self._deque.pop()


@singleton
class GlobalContextStack(ContextStack):
    pass


def get_global_context_stack() -> GlobalContextStack:
    instance = get_singleton_instance(GlobalContextStack)
    return instance if instance is not None else GlobalContextStack()


def get_latest_context() -> Optional[Context]:
    return get_global_context_stack().get()


def latest_context() -> Context:
    context = get_latest_context()
    if context is None:
        raise ValueError("The propagated context does not exist")
    return context


class ContextPropagator:
    def __init__(self, context: Context):
        self._stack = get_global_context_stack()
        self._context = context

    def __enter__(self):
        self._stack.push(self._context)
        return self._context

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stack.pop()

    async def __aenter__(self):
        self._stack.push(self._context)
        return self._context

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._stack.pop()

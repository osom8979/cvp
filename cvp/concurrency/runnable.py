# -*- coding: utf-8 -*-

from concurrent.futures import Executor, Future
from typing import Callable, Generic, Optional, ParamSpec, TypeVar
from weakref import ref

RunnableParamT = ParamSpec("RunnableParamT")
RunnableResultT = TypeVar("RunnableResultT")


class Runnable(Generic[RunnableParamT, RunnableResultT]):
    _future: Optional[Future[RunnableResultT]]
    _result: Optional[RunnableResultT]

    def __init__(
        self,
        executor: Executor,
        callback: Callable[RunnableParamT, RunnableResultT],
    ):
        self._executor = ref(executor)
        self._callback = callback
        self._running = False
        self._future = None
        self._result = None

    @property
    def running(self):
        return self._running

    @property
    def future(self):
        return self._future

    @property
    def result(self):
        return self._result

    def __bool__(self):
        return self.running

    def _done_callback(self, future: Future[RunnableResultT]) -> RunnableResultT:
        self._running = False
        self._result = future.result()
        return self._result

    def submit(
        self,
        *args: RunnableParamT.args,
        **kwargs: RunnableParamT.kwargs,
    ):
        if self._running:
            raise ValueError("Now running. Cannot be run repeatedly.")

        executor = self._executor()
        if executor is None:
            raise ReferenceError("The executor object has expired")

        assert isinstance(executor, Executor)

        self._running = True
        self._result = None
        self._future = executor.submit(self._callback, *args, **kwargs)
        self._future.add_done_callback(self._done_callback)
        return self._future

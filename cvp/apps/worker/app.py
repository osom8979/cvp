# -*- coding: utf-8 -*-

from argparse import Namespace
from asyncio import sleep
from multiprocessing.queues import Queue
from typing import Optional

from cvp.aio.run import aio_run
from cvp.logging.logging import worker_logger as logger
from cvp.msg import Message


class WorkerApplication:
    _queue: Optional[Queue[Message]]

    def __init__(self, *args, queue: Optional[Queue] = None, use_uvloop=False):
        self._args = args
        self._queue = queue
        self._use_uvloop = use_uvloop

    @classmethod
    def from_namespace(cls, args: Namespace):
        assert isinstance(args.use_uvloop, bool)
        assert isinstance(args.opts, list)
        return cls(*args.opts, queue=None, use_uvloop=args.use_uvloop)

    async def on_main(self):
        logger.debug(f"Initial arguments: {self._args}")
        try:
            while True:
                await sleep(1.0)
        finally:
            if self._queue is not None:
                self._queue.cancel_join_thread()

    def start(self) -> None:
        try:
            aio_run(self.on_main(), self._use_uvloop)
        except KeyboardInterrupt as e:
            logger.warning(e)

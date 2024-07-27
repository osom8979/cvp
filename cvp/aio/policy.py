# -*- coding: utf-8 -*-

from asyncio import (
    AbstractEventLoopPolicy,
    get_event_loop_policy,
    set_event_loop_policy,
)
from typing import Optional


class RestoreEventLoopPolicy:
    def __init__(self, policy: Optional[AbstractEventLoopPolicy] = None):
        self._policy = policy if policy is not None else get_event_loop_policy()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        set_event_loop_policy(self._policy)

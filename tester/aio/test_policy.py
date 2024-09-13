# -*- coding: utf-8 -*-

from asyncio import DefaultEventLoopPolicy, get_event_loop_policy, set_event_loop_policy
from unittest import TestCase, main

from uvloop import EventLoopPolicy as UvLoopEventLoopPolicy

from cvp.aio.policy import RestoreEventLoopPolicy


class PolicyTestCase(TestCase):
    def test_restore_event_loop_policy(self):
        prev_policy = get_event_loop_policy()
        self.assertIsInstance(prev_policy, DefaultEventLoopPolicy)

        with RestoreEventLoopPolicy():
            set_event_loop_policy(UvLoopEventLoopPolicy())
            uv_policy = get_event_loop_policy()
            self.assertIsInstance(uv_policy, UvLoopEventLoopPolicy)

        next_policy = get_event_loop_policy()
        self.assertIsInstance(next_policy, DefaultEventLoopPolicy)


if __name__ == "__main__":
    main()

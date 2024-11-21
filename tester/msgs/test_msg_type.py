# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.msgs.msg_type import MsgType


class MsgTypeTestCase(TestCase):
    def test_enum_values(self):
        self.assertEqual(0, MsgType.none)
        self.assertEqual(1, MsgType.toast)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.flow.enums.action import (
    FlowAction,
    normalize_action_name,
    normalize_action_value,
)


class ActionTestCase(TestCase):
    def test_normalize_action_name(self):
        self.assertEqual("flow", normalize_action_name(None))
        self.assertEqual("flow", normalize_action_name(FlowAction.flow))
        self.assertEqual("data", normalize_action_name(FlowAction.data))
        self.assertEqual("flow", normalize_action_name("flow"))
        self.assertEqual("data", normalize_action_name("data"))
        self.assertEqual("flow", normalize_action_name(0))
        self.assertEqual("data", normalize_action_name(1))

    def test_normalize_action_value(self):
        self.assertEqual(0, normalize_action_value(None))
        self.assertEqual(0, normalize_action_value(FlowAction.flow))
        self.assertEqual(1, normalize_action_value(FlowAction.data))
        self.assertEqual(0, normalize_action_value("flow"))
        self.assertEqual(1, normalize_action_value("data"))
        self.assertEqual(0, normalize_action_value(0))
        self.assertEqual(1, normalize_action_value(1))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

from dataclasses import dataclass
from unittest import TestCase, main

from cvp.patterns.proxy import ValueProxy
from cvp.patterns.state_watcher import OneShotStateObserver, StateWatcher
from cvp.types import override


class _TestInteger(ValueProxy[int]):
    def __init__(self, value=0):
        self.value = value

    @override
    def get(self) -> int:
        return self.value

    @override
    def set(self, value: int) -> None:
        self.value = value


@dataclass
class _EventObject:
    hit_count: int = 0
    update_value: int = 0
    prev_value: int = 0


class StateWatcherTestCase(TestCase):
    def test_default(self):
        watcher = StateWatcher()
        self.assertFalse(watcher)
        self.assertEqual(0, len(watcher))

        event_object = _EventObject()

        def _on_update(value: int, prev: int) -> None:
            event_object.hit_count += 1
            event_object.update_value = value
            event_object.prev_value = prev

        item = _TestInteger(100)
        watcher.oneshot(item, _on_update)
        self.assertTrue(watcher)
        self.assertEqual(1, len(watcher))

        result0 = watcher.update()
        self.assertFalse(result0)
        self.assertEqual(0, len(result0))

        self.assertEqual(0, event_object.hit_count)
        self.assertEqual(0, event_object.update_value)
        self.assertEqual(0, event_object.prev_value)
        self.assertEqual(100, item.value)

        item.value = 200
        result1 = watcher.update()
        self.assertTrue(result1)
        self.assertEqual(1, len(result1))

        observer0 = result1[0]
        self.assertIsInstance(observer0, OneShotStateObserver)
        self.assertEqual(item, observer0.proxy)
        self.assertEqual(200, observer0.prev_value)

        self.assertEqual(1, event_object.hit_count)
        self.assertEqual(200, event_object.update_value)
        self.assertEqual(100, event_object.prev_value)
        self.assertEqual(200, item.value)

        self.assertFalse(watcher)
        self.assertEqual(0, len(watcher))


if __name__ == "__main__":
    main()

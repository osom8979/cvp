# -*- coding: utf-8 -*-

from pathlib import Path
from unittest import TestCase, main

from cvp.containers.mapping_deque import MappingDeque


class MappingDequeTestCase(TestCase):
    def test_default(self):
        deque = MappingDeque[str, Path]()

        self.assertFalse(deque)
        self.assertEqual(len(deque), 0)
        self.assertNotIn("/", deque)

        deque.append(Path("/"))
        self.assertTrue(deque)
        self.assertEqual(len(deque), 1)
        self.assertIn("/", deque)

        deque.pop()
        self.assertFalse(deque)
        self.assertEqual(len(deque), 0)
        self.assertNotIn("/", deque)


if __name__ == "__main__":
    main()

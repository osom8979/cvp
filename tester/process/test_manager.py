# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.process.manager import ProcessManager


class ManagerTestCase(TestCase):
    def test_default(self):
        manager = ProcessManager()
        self.assertIsNotNone(manager)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.resources.home import HomeDir


class HomeTestCase(TestCase):
    def test_default(self):
        self.assertTrue(str(HomeDir.from_path()))


if __name__ == "__main__":
    main()

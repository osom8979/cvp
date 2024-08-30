# -*- coding: utf-8 -*-

from pathlib import Path
from unittest import TestCase, main

from cvp.resources.home import DEFAULT_CVP_HOME_PATH, HomeDir


class HomeTestCase(TestCase):
    def test_default(self):
        self.assertEqual(Path(DEFAULT_CVP_HOME_PATH), HomeDir.from_path())


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from cvp.resources.home import HomeDir


class HomeTestCase(TestCase):
    def test_default(self):
        with TemporaryDirectory() as tmpdir:
            self.assertTrue(os.path.isdir(tmpdir))
            self.assertTrue(HomeDir(tmpdir).is_dir())


if __name__ == "__main__":
    main()

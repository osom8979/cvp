# -*- coding: utf-8 -*-

import os
from unittest import TestCase, main

from cvp.renderer.modules import find_libsdl2_path


class ModulesTestCase(TestCase):
    def test_find_paths(self):
        self.assertTrue(os.path.isfile(find_libsdl2_path()))


if __name__ == "__main__":
    main()

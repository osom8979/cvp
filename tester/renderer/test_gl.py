# -*- coding: utf-8 -*-

from ctypes import CDLL
from unittest import TestCase, main

from cvp.renderer.gl import get_opengl_dll, get_process_address


class GlTestCase(TestCase):
    def test_get_opengl_dll(self):
        self.assertIsInstance(get_opengl_dll(), CDLL)

    def test_get_process_address(self):
        self.assertNotEquals(0, get_process_address("glGetString"))


if __name__ == "__main__":
    main()

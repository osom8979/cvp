# -*- coding: utf-8 -*-

from unittest import TestCase, main

from pygame.color import Color

from cvp.inspect.member import get_public_instance_attributes
from cvp.pygame import colors
from cvp.pygame.colors import color_to_hex_code


class ColorsTestCase(TestCase):
    def test_colors_type(self):
        for key, color in get_public_instance_attributes(colors):
            self.assertIsInstance(key, str)
            self.assertGreaterEqual(len(key), 1)
            self.assertIsInstance(color, tuple)
            self.assertEqual(len(color), 4)
            self.assertTrue(0 <= color[0] <= 255)
            self.assertTrue(0 <= color[1] <= 255)
            self.assertTrue(0 <= color[2] <= 255)
            self.assertTrue(0 <= color[3] <= 255)

    def test_color_to_hex_code(self):
        self.assertEqual("#FF0000FF", color_to_hex_code(Color("red")))
        self.assertEqual("#00FF00FF", color_to_hex_code(Color("green")))
        self.assertEqual("#0000FFFF", color_to_hex_code(Color("blue")))
        self.assertEqual("#000000FF", color_to_hex_code(Color("black")))
        self.assertEqual("#FFFFFFFF", color_to_hex_code(Color("white")))


if __name__ == "__main__":
    main()

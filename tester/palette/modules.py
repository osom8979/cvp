# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.palette import (
    basic_palette,
    css4_palette,
    extended_palette,
    flat_palette,
    registered_color_count,
    registered_palette_keys,
    tableau_palette,
    xkcd_palette,
)


class ModulesTestCase(TestCase):
    def test_default(self):
        expect_names = {"basic", "css4", "extended", "flat", "tableau", "xkcd"}
        actual_names = set(registered_palette_keys())
        self.assertSetEqual(expect_names, actual_names)

    def test_basic(self):
        self.assertEqual(16, len(basic_palette()))

    def test_css4(self):
        self.assertEqual(148, len(css4_palette()))

    def test_extended(self):
        self.assertEqual(140, len(extended_palette()))

    def test_flat(self):
        self.assertEqual(240, len(flat_palette()))

    def test_tableau(self):
        self.assertEqual(10, len(tableau_palette()))

    def test_xkcd(self):
        self.assertEqual(938, len(xkcd_palette()))

    def test_registered_color_count(self):
        expect_count = sum(
            (
                len(basic_palette()),
                len(css4_palette()),
                len(extended_palette()),
                len(flat_palette()),
                len(tableau_palette()),
                len(xkcd_palette()),
            )
        )
        self.assertEqual(expect_count, registered_color_count())


if __name__ == "__main__":
    main()

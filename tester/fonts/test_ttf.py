# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from cvp.fonts.ranges import read_ranges
from cvp.fonts.ttf import TTF


class TtfTestCase(TestCase):
    def test_jbm_ranges(self):
        jbm = TTF.from_jbm_nl_nfm_r()
        jbm_font_ranges = jbm.get_glyph_ranges()
        jbm_file_ranges = jbm.read_default_ranges()
        self.assertListEqual(jbm_font_ranges, jbm_file_ranges)

    def test_mdi_ranges(self):
        mdi = TTF.from_mdi()
        mdi_font_ranges = mdi.get_glyph_ranges()
        mdi_file_ranges = mdi.read_default_ranges()
        self.assertListEqual(mdi_font_ranges, mdi_file_ranges)

    def test_ngc_n_ranges(self):
        ngc_n = TTF.from_ngc()
        ngc_n_font_ranges = ngc_n.get_glyph_ranges()
        ngc_n_file_ranges = ngc_n.read_default_ranges()
        self.assertListEqual(ngc_n_font_ranges, ngc_n_file_ranges)

    def test_ngc_b_ranges(self):
        ngc_b = TTF.from_ngc_b()
        ngc_b_font_ranges = ngc_b.get_glyph_ranges()
        ngc_b_file_ranges = ngc_b.read_default_ranges()
        self.assertListEqual(ngc_b_font_ranges, ngc_b_file_ranges)

    def test_write_ranges(self):
        jbm = TTF.from_jbm_nl_nfm_r()
        with TemporaryDirectory() as tmpdir:
            self.assertTrue(os.path.isdir(tmpdir))
            ranges_file = os.path.join(tmpdir, "range")
            self.assertLess(0, jbm.write_ranges(ranges_file))
            ranges = read_ranges(ranges_file)
            self.assertListEqual(ranges, jbm.get_glyph_ranges())


if __name__ == "__main__":
    main()

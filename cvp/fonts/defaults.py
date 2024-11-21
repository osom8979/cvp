# -*- coding: utf-8 -*-

from cvp.assets import (
    get_jbm_nl_nfm_r_font_path,
    get_jbm_nl_nfm_r_font_ranges_path,
    get_mdi_font_path,
    get_mdi_font_ranges_path,
    get_ngc_b_font_path,
    get_ngc_b_font_ranges_path,
    get_ngc_font_path,
    get_ngc_font_ranges_path,
)
from cvp.fonts.ttf import TTF


def create_jbm_nl_nfm_r_ttf():
    return TTF(get_jbm_nl_nfm_r_font_path())


def create_mdi_ttf():
    return TTF(get_mdi_font_path())


def create_ngc_ttf():
    return TTF(get_ngc_font_path())


def create_ngc_b_ttf():
    return TTF(get_ngc_b_font_path())


def _write_default_font_ranges() -> None:
    create_jbm_nl_nfm_r_ttf().write_ranges(get_jbm_nl_nfm_r_font_ranges_path())
    create_mdi_ttf().write_ranges(get_mdi_font_ranges_path())
    create_ngc_ttf().write_ranges(get_ngc_font_ranges_path())
    create_ngc_b_ttf().write_ranges(get_ngc_b_font_ranges_path())


def _write_default_font_glyphs() -> None:
    # TODO
    pass


def _write_default_cache_files(verbose=False) -> None:
    if verbose:
        print("Writing ranges file...")
    _write_default_font_ranges()
    if verbose:
        print("Completed writing the ranges file.")

    if verbose:
        print("Writing glyphs file...")
    _write_default_font_glyphs()
    if verbose:
        print("Completed writing the glyphs file.")


if __name__ == "__main__":
    _write_default_cache_files(verbose=True)

# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final


@unique
class Crf(IntEnum):
    """
    Constant Rate Factor

    Choose a CRF value:
        The range of the CRF scale is 0–51, where 0 is lossless (for 8 bit only, for 10
        bit use -qp 0), 23 is the default, and 51 is worst quality possible. A lower
        value generally leads to higher quality, and a subjectively sane range is 17–28.
        Consider 17 or 18 to be visually lossless or nearly so; it should look the same
        or nearly the same as the input but it isn't technically lossless.

        The range is exponential, so increasing the CRF value +6 results in roughly half
        the bitrate / file size, while -6 leads to roughly twice the bitrate.

        Choose the highest CRF value that still provides an acceptable quality. If the
        output looks good, then try a higher value. If it looks bad, choose a lower
        value.

    References:
        https://trac.ffmpeg.org/wiki/Encode/H.264#crf
    """

    lossless = 0  # for 8 bit only, for 10 bit use -qp 0
    visually_lossless = 17
    default = 23
    worst_quality_possible = 51
    sane_range_min = 17
    sane_range_max = 28


CRF_MIN: Final[Crf] = Crf.lossless
CRF_MAX: Final[Crf] = Crf.worst_quality_possible
CRF_DEFAULT: Final[Crf] = Crf.default

# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class Profile(StrEnum):
    """
    https://trac.ffmpeg.org/wiki/Encode/H.264#Profile
    """

    baseline = auto()
    main = auto()
    high = auto()
    high10 = auto()
    high422 = auto()
    high444 = auto()

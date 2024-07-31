# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Final


@unique
class Preset(StrEnum):
    """
    https://trac.ffmpeg.org/wiki/Encode/H.264#Preset
    """

    ultrafast = auto()
    superfast = auto()
    veryfast = auto()
    faster = auto()
    fast = auto()
    medium = auto()  # default preset
    preset = auto()
    slow = auto()
    slower = auto()
    veryslow = auto()
    placebo = auto()  # ignore this as it is not useful


DEFAULT_PRESET: Final[Preset] = Preset.medium

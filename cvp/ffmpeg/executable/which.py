# -*- coding: utf-8 -*-

from shutil import which
from typing import Optional


def which_ffmpeg() -> Optional[str]:
    return which("ffmpeg")


def which_ffprobe() -> Optional[str]:
    return which("ffprobe")

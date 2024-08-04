# -*- coding: utf-8 -*-

import os
from functools import lru_cache
from typing import Optional

from cvp.assets.download import DEFAULT_DOWNLOAD_TIMEOUT
from cvp.ffmpeg.executable.links import get_ffmpeg_link, get_ffprobe_link
from cvp.ffmpeg.executable.which import which_ffmpeg, which_ffprobe


def has_ffmpeg():
    if which_ffmpeg():
        return True
    else:
        return get_ffmpeg_link().has_extract_files


def has_ffprobe():
    if which_ffprobe():
        return True
    else:
        return get_ffprobe_link().has_extract_files


def prepare_ffmpeg(timeout: Optional[float] = DEFAULT_DOWNLOAD_TIMEOUT) -> str:
    path = which_ffmpeg()
    if path:
        return path

    link = get_ffmpeg_link()
    link.prepare(timeout=timeout)

    files = link.extract_files
    assert 1 == len(link.paths)

    path = files[0]
    if not os.access(path, os.X_OK):
        raise PermissionError(f"'{path}' is not executable")

    return path


def prepare_ffprobe(timeout: Optional[float] = DEFAULT_DOWNLOAD_TIMEOUT) -> str:
    path = which_ffprobe()
    if path:
        return path

    link = get_ffprobe_link()
    link.prepare(timeout=timeout)

    files = link.extract_files
    assert 1 == len(link.paths)

    path = files[0]
    if not os.access(path, os.X_OK):
        raise PermissionError(f"'{path}' is not executable")

    return path


@lru_cache
def get_ffmpeg_executable() -> Optional[str]:
    try:
        return prepare_ffmpeg()
    except:  # noqa
        return None


@lru_cache
def get_ffprobe_executable() -> Optional[str]:
    try:
        return prepare_ffprobe()
    except:  # noqa
        return None

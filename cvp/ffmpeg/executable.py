# -*- coding: utf-8 -*-

import os
from enum import StrEnum, auto, unique
from shutil import which
from sys import platform
from typing import Dict, Final, NamedTuple, Optional
from urllib.request import urlopen


def which_ffmpeg() -> Optional[str]:
    return which("ffmpeg")


def which_ffprobe() -> Optional[str]:
    return which("ffprobe")


class UrlMd5(NamedTuple):
    url: str
    md5: str


@unique
class _Platform(StrEnum):
    win32 = auto()
    darwin = auto()
    linux = auto()


_FFMPEG_DOWNLOAD_INFOS: Final[Dict[str, UrlMd5]] = {
    _Platform.win32: UrlMd5("", ""),
    _Platform.darwin: UrlMd5("", ""),
    _Platform.linux: UrlMd5("", ""),
}

_FFPROBE_DOWNLOAD_INFOS: Final[Dict[str, UrlMd5]] = {
    _Platform.win32: UrlMd5("", ""),
    _Platform.darwin: UrlMd5("", ""),
    _Platform.linux: UrlMd5("", ""),
}


def _download_file(
    url: str,
    md5: str,
    filename: str,
    cache_dir: Optional[str] = None,
    timeout: Optional[float] = None,
) -> None:
    try:
        request = urlopen(url, timeout=timeout)
        with open(filename, "wb") as f:
            f.write(request.read())
    except:  # noqa
        os.remove(filename)


def download_ffmpeg(path: str, timeout: Optional[float] = None):
    if platform not in _FFMPEG_DOWNLOAD_INFOS:
        raise OSError("This platform does not support static-ffmpeg downloads")

    info = _FFMPEG_DOWNLOAD_INFOS[platform]
    _download_file(info.url, info.md5, path, timeout=timeout)


def download_ffprobe(path: str, timeout: Optional[float] = None):
    if platform not in _FFPROBE_DOWNLOAD_INFOS:
        raise OSError("This platform does not support static-ffprobe downloads")

    info = _FFPROBE_DOWNLOAD_INFOS[platform]
    _download_file(info.url, info.md5, path, timeout=timeout)

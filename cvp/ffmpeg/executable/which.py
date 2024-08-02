# -*- coding: utf-8 -*-

import os
import platform
from enum import StrEnum, unique
from shutil import which
from typing import Dict, Final, NamedTuple, Optional
from urllib.request import urlopen


def which_ffmpeg() -> Optional[str]:
    return which("ffmpeg")


def which_ffprobe() -> Optional[str]:
    return which("ffprobe")


# def _download_file(
#     url: str,
#     sha1: str,
#     source_path: str,
#     destination_path: str,
#     cache_dir: str,
#     timeout: Optional[float] = None,
# ) -> None:
#     filename = ""
#     try:
#         request = urlopen(url, timeout=timeout)
#         with open(filename, "wb") as f:
#             f.write(request.read())
#     except:  # noqa
#         os.remove(filename)
#
#
# def _download_link(
#     link: LinkInfo,
#     destination_path: str,
#     cache_dir: str,
#     timeout: Optional[float] = None,
# ) -> None:
#     _download_file(
#         url=link.url,
#         sha1=link.sha1,
#         source_path=link.path,
#         destination_path=destination_path,
#         cache_dir=cache_dir,
#         timeout=timeout,
#     )
#
#
# def download_ffmpeg(
#     destination_path: str,
#     cache_dir: str,
#     timeout: Optional[float] = None,
# ):
#     sm = get_system_machine()
#     if sm not in _FFMPEG_LINKS:
#         raise OSError("This platform does not support static-ffmpeg downloads")
#     _download_link(
#         link=_FFMPEG_LINKS[sm],
#         destination_path=destination_path,
#         cache_dir=cache_dir,
#         timeout=timeout,
#     )
#
#
# def download_ffprobe(
#     destination_path: str,
#     cache_dir: str,
#     timeout: Optional[float] = None,
# ):
#     sm = get_system_machine()
#     if sm not in _FFPROBE_LINKS:
#         raise OSError("This platform does not support static-ffprobe downloads")
#     _download_link(
#         link=_FFPROBE_LINKS[sm],
#         destination_path=destination_path,
#         cache_dir=cache_dir,
#         timeout=timeout,
#     )

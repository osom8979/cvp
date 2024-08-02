# -*- coding: utf-8 -*-

from typing import Dict, Final, NamedTuple, Optional

from cvp.ffmpeg.executable.links import BtbN
from cvp.ffmpeg.executable.links import evermeet
from cvp.system.platform import SysMach, get_system_machine


class LinkInfo(NamedTuple):
    url: str
    sha1: str
    path: str
    license: str


_FFMPEG_LINKS: Final[Dict[str, LinkInfo]] = {
    SysMach.windows_x64: LinkInfo(
        BtbN.WIN64_URL,
        BtbN.WIN64_SHA1,
        BtbN.WIN64_FFMPEG_SUB_PATH,
        BtbN.WIN64_LICENSE,
    ),
    SysMach.linux_x64: LinkInfo(
        BtbN.LINUX64_URL,
        BtbN.LINUX64_SHA1,
        BtbN.LINUX64_FFMPEG_SUB_PATH,
        BtbN.LINUX64_LICENSE,
    ),
    SysMach.darwin_x64: LinkInfo(
        evermeet.FFMPEG_URL,
        evermeet.FFMPEG_SHA1,
        evermeet.FFMPEG_SUB_PATH,
        evermeet.FFMPEG_LICENSE,
    ),
}

_FFPROBE_LINKS: Final[Dict[str, LinkInfo]] = {
    SysMach.windows_x64: LinkInfo(
        BtbN.WIN64_URL,
        BtbN.WIN64_SHA1,
        BtbN.WIN64_FFPROBE_SUB_PATH,
        BtbN.WIN64_LICENSE,
    ),
    SysMach.linux_x64: LinkInfo(
        BtbN.LINUX64_URL,
        BtbN.LINUX64_SHA1,
        BtbN.LINUX64_FFPROBE_SUB_PATH,
        BtbN.LINUX64_LICENSE,
    ),
    SysMach.darwin_x64: LinkInfo(
        evermeet.FFPROBE_URL,
        evermeet.FFPROBE_SHA1,
        evermeet.FFPROBE_SUB_PATH,
        evermeet.FFPROBE_LICENSE,
    ),
}


class PairInfo(NamedTuple):
    ffmpeg: LinkInfo
    ffprobe: LinkInfo


_KEYS = tuple(_FFMPEG_LINKS.keys())
_LINKS = {k: PairInfo(_FFMPEG_LINKS[k], _FFPROBE_LINKS[k]) for k in _KEYS}


def get_link(sm: Optional[SysMach] = None) -> PairInfo:
    sm = sm if sm else get_system_machine()
    assert sm is not None

    if sm not in _LINKS:
        raise OSError(f"{sm} platform does not support ffmpeg downloads")

    return _LINKS[sm]


def get_ffmpeg_link(sm: Optional[SysMach] = None) -> LinkInfo:
    return get_link(sm).ffmpeg


def get_ffprobe_link(sm: Optional[SysMach] = None) -> LinkInfo:
    return get_link(sm).ffprobe

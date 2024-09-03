# -*- coding: utf-8 -*-

from typing import Dict, Final, NamedTuple, Optional, Sequence, Tuple, Union

from cvp.ffmpeg.static.links import BtbN, evermeet
from cvp.system.platform import SysMach, get_system_machine


class ExtractInfo(NamedTuple):
    src: str
    dest: str


class LinkInfo(NamedTuple):
    url: str
    paths: Sequence[Union[Tuple[str, str], ExtractInfo]]
    checksum: str


class PairInfo(NamedTuple):
    ffmpeg: LinkInfo
    ffprobe: LinkInfo


FFMPEG_LINKS: Final[Dict[str, LinkInfo]] = {
    SysMach.windows_x64: LinkInfo(
        url=BtbN.WIN64_URL,
        paths=[(BtbN.WIN64_FFMPEG_SUB_PATH, "bin/ffmpeg.exe")],
        checksum=BtbN.WIN64_CHECKSUM,
    ),
    SysMach.linux_x64: LinkInfo(
        url=BtbN.LINUX64_URL,
        paths=[(BtbN.LINUX64_FFMPEG_SUB_PATH, "bin/ffmpeg")],
        checksum=BtbN.LINUX64_CHECKSUM,
    ),
    SysMach.darwin_x64: LinkInfo(
        url=evermeet.FFMPEG_URL,
        paths=[(evermeet.FFMPEG_SUB_PATH, "bin/ffmpeg")],
        checksum=evermeet.FFMPEG_CHECKSUM,
    ),
}

FFPROBE_LINKS: Final[Dict[str, LinkInfo]] = {
    SysMach.windows_x64: LinkInfo(
        url=BtbN.WIN64_URL,
        paths=[(BtbN.WIN64_FFPROBE_SUB_PATH, "bin/ffprobe.exe")],
        checksum=BtbN.WIN64_CHECKSUM,
    ),
    SysMach.linux_x64: LinkInfo(
        url=BtbN.LINUX64_URL,
        paths=[(BtbN.LINUX64_FFPROBE_SUB_PATH, "bin/ffprobe")],
        checksum=BtbN.LINUX64_CHECKSUM,
    ),
    SysMach.darwin_x64: LinkInfo(
        url=evermeet.FFPROBE_URL,
        paths=[(evermeet.FFPROBE_SUB_PATH, "bin/ffprobe")],
        checksum=evermeet.FFPROBE_CHECKSUM,
    ),
}

KEYS = tuple(FFMPEG_LINKS.keys())
LINKS = {k: PairInfo(FFMPEG_LINKS[k], FFPROBE_LINKS[k]) for k in KEYS}


def get_link(sm: Optional[SysMach] = None) -> PairInfo:
    sm = sm if sm else get_system_machine()
    assert sm is not None

    if sm not in LINKS:
        raise OSError(f"{sm} platform does not support ffmpeg downloads")

    return LINKS[sm]


def get_ffmpeg_link(sm: Optional[SysMach] = None) -> LinkInfo:
    return get_link(sm).ffmpeg


def get_ffprobe_link(sm: Optional[SysMach] = None) -> LinkInfo:
    return get_link(sm).ffprobe

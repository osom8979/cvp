# -*- coding: utf-8 -*-

from typing import Dict, Final, NamedTuple, Optional

from cvp.assets.download import DownloadArchive
from cvp.ffmpeg.executable.links import BtbN, evermeet
from cvp.system.platform import SysMach, get_system_machine

_FFMPEG_LINKS: Final[Dict[str, DownloadArchive]] = {
    SysMach.windows_x64: DownloadArchive(
        url=BtbN.WIN64_URL,
        paths=[(BtbN.WIN64_FFMPEG_SUB_PATH, "bin/ffmpeg.exe")],
        checksum=BtbN.WIN64_CHECKSUM,
    ),
    SysMach.linux_x64: DownloadArchive(
        url=BtbN.LINUX64_URL,
        paths=[(BtbN.LINUX64_FFMPEG_SUB_PATH, "bin/ffmpeg")],
        checksum=BtbN.LINUX64_CHECKSUM,
    ),
    SysMach.darwin_x64: DownloadArchive(
        url=evermeet.FFMPEG_URL,
        paths=[(evermeet.FFMPEG_SUB_PATH, "bin/ffmpeg")],
        checksum=evermeet.FFMPEG_CHECKSUM,
    ),
}

_FFPROBE_LINKS: Final[Dict[str, DownloadArchive]] = {
    SysMach.windows_x64: DownloadArchive(
        url=BtbN.WIN64_URL,
        paths=[(BtbN.WIN64_FFPROBE_SUB_PATH, "bin/ffprobe.exe")],
        checksum=BtbN.WIN64_CHECKSUM,
    ),
    SysMach.linux_x64: DownloadArchive(
        url=BtbN.LINUX64_URL,
        paths=[(BtbN.LINUX64_FFPROBE_SUB_PATH, "bin/ffprobe")],
        checksum=BtbN.LINUX64_CHECKSUM,
    ),
    SysMach.darwin_x64: DownloadArchive(
        url=evermeet.FFPROBE_URL,
        paths=[(evermeet.FFPROBE_SUB_PATH, "bin/ffprobe")],
        checksum=evermeet.FFPROBE_CHECKSUM,
    ),
}


class PairInfo(NamedTuple):
    ffmpeg: DownloadArchive
    ffprobe: DownloadArchive


_KEYS = tuple(_FFMPEG_LINKS.keys())
_LINKS = {k: PairInfo(_FFMPEG_LINKS[k], _FFPROBE_LINKS[k]) for k in _KEYS}


def get_link(sm: Optional[SysMach] = None) -> PairInfo:
    sm = sm if sm else get_system_machine()
    assert sm is not None

    if sm not in _LINKS:
        raise OSError(f"{sm} platform does not support ffmpeg downloads")

    return _LINKS[sm]


def get_ffmpeg_link(sm: Optional[SysMach] = None) -> DownloadArchive:
    return get_link(sm).ffmpeg


def get_ffprobe_link(sm: Optional[SysMach] = None) -> DownloadArchive:
    return get_link(sm).ffprobe

# -*- coding: utf-8 -*-

from typing import Dict, Final

from cvp.resources.download.links.ffmpeg import BtbN, evermeet
from cvp.resources.download.links.tuples import LinkInfo
from cvp.system.platform import SysMach

LinkMap = Dict[SysMach, LinkInfo]

FFMPEG_LINKS: Final[LinkMap] = {
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

FFPROBE_LINKS: Final[LinkMap] = {
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

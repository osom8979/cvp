# -*- coding: utf-8 -*-

import os
import platform
from enum import StrEnum, unique
from shutil import which
from typing import Dict, Final, NamedTuple, Optional
from urllib.request import urlopen

_windows = "windows"
_linux = "linux"
_darwin = "darwin"

_x64 = "x64"
_x86 = "x86"
_arm64 = "arm64"


@unique
class SysMach(StrEnum):
    win_x64 = f"{_windows}.{_x64}"
    win_x86 = f"{_windows}.{_x86}"
    win_a64 = f"{_windows}.{_arm64}"
    lnx_x64 = f"{_linux}.{_x64}"
    lnx_x86 = f"{_linux}.{_x86}"
    lnx_a64 = f"{_linux}.{_arm64}"
    mac_x64 = f"{_darwin}.{_x64}"
    mac_x86 = f"{_darwin}.{_x86}"
    mac_a64 = f"{_darwin}.{_arm64}"  # Apple Silicon ARM


class LinkInfo(NamedTuple):
    url: str
    path: str
    sha1: str
    license: str


_BtbN0 = "https://github.com/BtbN/FFmpeg-Builds/releases/download"
_BtbN1 = "autobuild-2024-07-31-12-50"

_BtbN2_WIN64 = "ffmpeg-n7.0.1-221-g0ab20b5788-win64-gpl-7.0"
_BtbN2_WIN64_EXT = ".zip"
_BtbN2_WIN64_SHA1 = "a2e8a546d6c6a113ea9b1fb8248a0ec235c80aba"
_BtbN2_WIN64_LICENSE = "gpl"

_BtbN2_LINUX64 = "ffmpeg-n7.0.1-221-g0ab20b5788-linux64-gpl-7.0"
_BtbN2_LINUX64_EXT = ".tar.xz"
_BtbN2_LINUX64_SHA1 = "75b56345226ace27f072750ce79d713e07686e8a"
_BtbN2_LINUX64_LICENSE = "gpl"

_FFMPEG_LINKS: Final[Dict[str, LinkInfo]] = {
    SysMach.win_x64: LinkInfo(
        f"{_BtbN0}/{_BtbN1}/{_BtbN2_WIN64}{_BtbN2_WIN64_EXT}",
        f"{_BtbN2_WIN64}/bin/ffmpeg.exe",
        _BtbN2_WIN64_SHA1,
        _BtbN2_WIN64_LICENSE,
    ),
    SysMach.lnx_x64: LinkInfo(
        f"{_BtbN0}/{_BtbN1}/{_BtbN2_LINUX64}{_BtbN2_LINUX64_EXT}",
        f"{_BtbN2_LINUX64}/bin/ffmpeg",
        _BtbN2_LINUX64_SHA1,
        _BtbN2_LINUX64_LICENSE,
    ),
    SysMach.mac_x64: LinkInfo(
        "https://evermeet.cx/pub/ffmpeg/ffmpeg-7.0.1.zip",
        "ffmpeg",
        "0dae4985ed0c32f4cfe7362b8b2bdfcd43bc4a9f",
        "gpl",
    ),
}

_FFPROBE_LINKS: Final[Dict[str, LinkInfo]] = {
    SysMach.win_x64: LinkInfo(
        f"{_BtbN0}/{_BtbN1}/{_BtbN2_WIN64}{_BtbN2_WIN64_EXT}",
        f"{_BtbN2_WIN64}/bin/ffprobe.exe",
        _BtbN2_WIN64_SHA1,
        _BtbN2_WIN64_LICENSE,
    ),
    SysMach.lnx_x64: LinkInfo(
        f"{_BtbN0}/{_BtbN1}/{_BtbN2_LINUX64}{_BtbN2_LINUX64_EXT}",
        f"{_BtbN2_LINUX64}/bin/ffprobe",
        _BtbN2_LINUX64_SHA1,
        _BtbN2_LINUX64_LICENSE,
    ),
    SysMach.mac_x64: LinkInfo(
        "https://evermeet.cx/ffmpeg/ffprobe-7.0.1.zip",
        "ffprobe",
        "3d494faa023b2f39a6a581758f793c7a68cced88",
        "gpl",
    ),
}


def get_normalized_system() -> str:
    match platform.system():
        case "Darwin":
            return _darwin
        case "Windows":
            return _windows
        case "Linux":
            return _linux
        case sys:
            raise ValueError(f"Unsupported platform: {sys}")


def get_normalized_machine() -> str:
    match platform.machine():
        case "x86_64":
            return _x64
        case "i386":
            return _x86
        case m if m in ("arm64", "aarch64"):
            return _arm64
        case m:
            raise ValueError(f"Unsupported machine: {m}")


def get_system_machine() -> SysMach:
    sys = get_normalized_system()
    mach = get_normalized_machine()
    return SysMach(f"{sys}.{mach}")


def which_ffmpeg() -> Optional[str]:
    return which("ffmpeg")


def which_ffprobe() -> Optional[str]:
    return which("ffprobe")


def _download_file(
    url: str,
    sha1: str,
    source_path: str,
    destination_path: str,
    cache_dir: str,
    timeout: Optional[float] = None,
) -> None:
    filename = ""
    try:
        request = urlopen(url, timeout=timeout)
        with open(filename, "wb") as f:
            f.write(request.read())
    except:  # noqa
        os.remove(filename)


def _download_link(
    link: LinkInfo,
    destination_path: str,
    cache_dir: str,
    timeout: Optional[float] = None,
) -> None:
    _download_file(
        url=link.url,
        sha1=link.sha1,
        source_path=link.path,
        destination_path=destination_path,
        cache_dir=cache_dir,
        timeout=timeout,
    )


def download_ffmpeg(
    destination_path: str,
    cache_dir: str,
    timeout: Optional[float] = None,
):
    sm = get_system_machine()
    if sm not in _FFMPEG_LINKS:
        raise OSError("This platform does not support static-ffmpeg downloads")
    _download_link(
        link=_FFMPEG_LINKS[sm],
        destination_path=destination_path,
        cache_dir=cache_dir,
        timeout=timeout,
    )


def download_ffprobe(
    destination_path: str,
    cache_dir: str,
    timeout: Optional[float] = None,
):
    sm = get_system_machine()
    if sm not in _FFPROBE_LINKS:
        raise OSError("This platform does not support static-ffprobe downloads")
    _download_link(
        link=_FFPROBE_LINKS[sm],
        destination_path=destination_path,
        cache_dir=cache_dir,
        timeout=timeout,
    )

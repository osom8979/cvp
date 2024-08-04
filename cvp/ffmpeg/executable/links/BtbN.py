# -*- coding: utf-8 -*-
# BtbN supports Windows and Linux.

HEALTHCHECK_URL = "https://github.com/BtbN/FFmpeg-Builds"

_0 = "https://github.com/BtbN/FFmpeg-Builds/releases/download"
_1 = "autobuild-2024-07-31-12-50"

_2_WIN64 = "ffmpeg-n7.0.1-221-g0ab20b5788-win64-gpl-7.0"
_2_WIN64_EXT = ".zip"
_2_WIN64_SHA1 = "a2e8a546d6c6a113ea9b1fb8248a0ec235c80aba"

_2_LINUX64 = "ffmpeg-n7.0.1-221-g0ab20b5788-linux64-gpl-7.0"
_2_LINUX64_EXT = ".tar.xz"
_2_LINUX64_SHA1 = "75b56345226ace27f072750ce79d713e07686e8a"

WIN64_URL = f"{_0}/{_1}/{_2_WIN64}{_2_WIN64_EXT}"
WIN64_CHECKSUM = f"sha1:{_2_WIN64_SHA1}"
WIN64_FFMPEG_SUB_PATH = f"{_2_WIN64}/bin/ffmpeg.exe"
WIN64_FFPROBE_SUB_PATH = f"{_2_WIN64}/bin/ffprobe.exe"

LINUX64_URL = f"{_0}/{_1}/{_2_LINUX64}{_2_LINUX64_EXT}"
LINUX64_CHECKSUM = f"sha1:{_2_LINUX64_SHA1}"
LINUX64_FFMPEG_SUB_PATH = f"{_2_LINUX64}/bin/ffmpeg"
LINUX64_FFPROBE_SUB_PATH = f"{_2_LINUX64}/bin/ffprobe"

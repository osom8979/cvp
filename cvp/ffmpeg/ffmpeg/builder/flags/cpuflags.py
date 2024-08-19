# -*- coding: utf-8 -*-
"""
Allows setting and clearing cpu flags.

This option is intended for testing.

Do not use it unless you know what you’re doing.

ffmpeg -cpuflags -sse+mmx ...
ffmpeg -cpuflags mmx ...
ffmpeg -cpuflags 0 ...

https://www.ffmpeg.org/ffmpeg.html#Generic-options
"""

from enum import StrEnum, auto, unique


@unique
class X86(StrEnum):
    mmx = auto()
    mmxext = auto()
    sse = auto()
    sse2 = auto()
    sse2slow = auto()
    sse3 = auto()
    sse3slow = auto()
    ssse3 = auto()
    atom = auto()
    sse4_1 = "sse4.1"
    sse4_2 = "sse4.2"
    avx = auto()
    avx2 = auto()
    xop = auto()
    fma3 = auto()
    fma4 = auto()
    now3d = "3dnow"
    now3dext = "3dnowext"
    bmi1 = auto()
    bmi2 = auto()
    cmov = auto()


@unique
class ARM(StrEnum):
    armv5te = auto()
    armv6 = auto()
    armv6t2 = auto()
    vfp = auto()
    vfpv3 = auto()
    neon = auto()
    setend = auto()


@unique
class AArch64(StrEnum):
    armv8 = auto()
    vfp = auto()
    neon = auto()


@unique
class PowerPC(StrEnum):
    altivec = auto()


@unique
class SpecificProcessors(StrEnum):
    pentium2 = auto()
    pentium3 = auto()
    pentium4 = auto()
    k6 = auto()
    k62 = auto()
    athlon = auto()
    athlonxp = auto()
    k8 = auto()

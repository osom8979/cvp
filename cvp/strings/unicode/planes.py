# -*- coding: utf-8 -*-

from typing import Final, NamedTuple, Sequence, Tuple

PLANE_INDEX_MIN: Final[int] = 0
PLANE_INDEX_MAX: Final[int] = 16


class UnicodePlane(NamedTuple):
    idx: int
    long: str
    short: str
    begin: int
    end: int

    @property
    def range(self) -> Tuple[int, int]:
        return self.begin, self.end

    def __repr__(self):
        return f"Plane {self.idx} {self.short}: U+{self.begin:04X} - U+{self.end:04X}"


class UnicodePlaneCategory(NamedTuple):
    long: str
    short: str
    begin: int
    end: int

    @property
    def range(self) -> Tuple[int, int]:
        return self.begin, self.end

    def __repr__(self):
        return f"{self.long} ({self.short}): U+{self.begin:04X} - U+{self.end:04X}"

    def make_plane(self, idx: int, begin: int, end: int) -> UnicodePlane:
        assert PLANE_INDEX_MIN <= idx <= PLANE_INDEX_MAX
        assert begin < end
        assert self.begin <= begin <= self.end
        assert self.begin <= end <= self.end
        return UnicodePlane(idx, self.long, self.short, begin, end)

    def __call__(self, idx: int) -> UnicodePlane:
        begin = idx * 0x10000
        end = begin + 0xFFFF
        return self.make_plane(idx, begin, end)


# fmt: off
BMP = UnicodePlaneCategory("Basic Multilingual Plane", "BMP", 0x0000, 0xFFFF)
SMP = UnicodePlaneCategory("Supplementary Multilingual Plane", "SMP", 0x10000, 0x1FFFF)
SIP = UnicodePlaneCategory("Supplementary Ideographic Plane", "SIP", 0x20000, 0x2FFFF)
TIP = UnicodePlaneCategory("Tertiary Ideographic Plane", "TIP", 0x30000, 0x3FFFF)
UNASSIGNED = UnicodePlaneCategory("Unassigned", "-", 0x40000, 0xDFFFF)
SSP = UnicodePlaneCategory("Supplementary Special-purpose Plane", "SSP", 0xE0000, 0xEFFFF)  # noqa: E501
PUA_A = UnicodePlaneCategory("Private Use Plane A", "PUA-A", 0xF0000, 0xFFFFF)
PUA_B = UnicodePlaneCategory("Private Use Plane B", "PUA-B", 0x100000, 0x10FFFF)
# fmt: on

PUA_AB = UnicodePlaneCategory(
    "Supplementary Private Use Area planes",
    "SPUA-A/B",
    PUA_A.begin,
    PUA_B.end,
)

PLANE0 = BMP(0)
PLANE1 = SMP(1)
PLANE2 = SIP(2)
PLANE3 = TIP(3)
PLANE4 = UNASSIGNED(4)
PLANE5 = UNASSIGNED(5)
PLANE6 = UNASSIGNED(6)
PLANE7 = UNASSIGNED(7)
PLANE8 = UNASSIGNED(8)
PLANE9 = UNASSIGNED(9)
PLANE10 = UNASSIGNED(10)
PLANE11 = UNASSIGNED(11)
PLANE12 = UNASSIGNED(12)
PLANE13 = UNASSIGNED(13)
PLANE14 = SSP(14)
PLANE15 = PUA_A(15)
PLANE16 = PUA_B(16)

PLANES: Sequence[UnicodePlane] = (
    PLANE0,
    PLANE1,
    PLANE2,
    PLANE3,
    PLANE4,
    PLANE5,
    PLANE6,
    PLANE7,
    PLANE8,
    PLANE9,
    PLANE10,
    PLANE11,
    PLANE12,
    PLANE13,
    PLANE14,
    PLANE15,
    PLANE16,
)

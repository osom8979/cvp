# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Plane_(Unicode)

from typing import Final, NamedTuple, Sequence, Tuple

PLANE_INDEX_MIN: Final[int] = 0
PLANE_INDEX_MAX: Final[int] = 16

MAXIMUM_CODE_POINTS: Final[int] = 65_536
assert MAXIMUM_CODE_POINTS == 0x10000
assert MAXIMUM_CODE_POINTS - 1 == 0xFFFF

UNASSIGNED_PLANE_INDEX_MIN: Final[int] = 4
UNASSIGNED_PLANE_INDEX_MAX: Final[int] = 13


class UnicodePlane(NamedTuple):
    number: int
    long_name: str
    short_name: str
    begin: int
    end: int

    @property
    def range(self) -> Tuple[int, int]:
        return self.begin, self.end

    def __repr__(self):
        return f"{self.number} {self.short_name}: U+{self.begin:04X} - U+{self.end:04X}"


def _plane_range(number: int) -> Tuple[int, int]:
    assert PLANE_INDEX_MIN <= number <= PLANE_INDEX_MAX
    begin = number * MAXIMUM_CODE_POINTS
    end = begin + MAXIMUM_CODE_POINTS - 1
    return begin, end


def _plane(number: int, long_name: str, short_name: str) -> UnicodePlane:
    begin, end = _plane_range(number)
    return UnicodePlane(number, long_name, short_name, begin, end)


def _unassigned(number: int) -> UnicodePlane:
    assert UNASSIGNED_PLANE_INDEX_MIN <= number <= UNASSIGNED_PLANE_INDEX_MAX
    return _plane(number, "Unassigned", "-")


PLANE0 = _plane(0, "Basic Multilingual Plane", "BMP")
PLANE1 = _plane(1, "Supplementary Multilingual Plane", "SMP")
PLANE2 = _plane(2, "Supplementary Ideographic Plane", "SIP")
PLANE3 = _plane(3, "Tertiary Ideographic Plane", "TIP")
PLANE4 = _unassigned(4)
PLANE5 = _unassigned(5)
PLANE6 = _unassigned(6)
PLANE7 = _unassigned(7)
PLANE8 = _unassigned(8)
PLANE9 = _unassigned(9)
PLANE10 = _unassigned(10)
PLANE11 = _unassigned(11)
PLANE12 = _unassigned(12)
PLANE13 = _unassigned(13)
PLANE14 = _plane(14, "Supplementary Special-purpose Plane", "SSP")
PLANE15 = _plane(15, "Private Use Plane A", "PUA-A")
PLANE16 = _plane(16, "Private Use Plane B", "PUA-B")

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

BMP = PLANE0
SMP = PLANE1
SIP = PLANE2
TIP = PLANE3
SSP = PLANE14
PUA_A = PLANE15
PUA_B = PLANE16

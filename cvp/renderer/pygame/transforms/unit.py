# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import IntEnum
from typing import Sequence as _TypingSequence
from typing import Tuple


class TransformUnit(IntEnum):
    RATIO = 0
    ABSOLUTE = 1


@dataclass
class PointUnit:
    x: float = 0.0
    y: float = 0.0
    unit: TransformUnit = TransformUnit.RATIO

    @classmethod
    def from_any(cls, value):
        if not value:
            return cls()

        assert value is not None
        if isinstance(value, cls):
            return cls(value.x, value.y, value.unit)

        if not isinstance(value, _TypingSequence):
            raise TypeError(f"Unsupported sequence type: {type(value).__name__}")

        x = value[0] if len(value) >= 1 else 0.0
        y = value[1] if len(value) >= 2 else 0.0
        unit = value[2] if len(value) >= 3 else TransformUnit.RATIO
        return cls(x=x, y=y, unit=unit)

    def calc(self, size: Tuple[float, float]):
        if self.unit == TransformUnit.ABSOLUTE:
            return self.x, self.y
        else:
            assert self.unit == TransformUnit.RATIO
            return self.x * size[0], self.y * size[1]


@dataclass
class RectUnit:
    x: float = 0.0
    y: float = 0.0
    width: float = 1.0
    height: float = 1.0
    unit: TransformUnit = TransformUnit.RATIO

    @classmethod
    def from_any(cls, value):
        if not value:
            return cls()

        assert value is not None
        if isinstance(value, cls):
            return cls(value.x, value.y, value.width, value.height, value.unit)

        if not isinstance(value, _TypingSequence):
            raise TypeError(f"Unsupported sequence type: {type(value).__name__}")

        x = value[0] if len(value) >= 1 else 0.0
        y = value[1] if len(value) >= 2 else 0.0
        width = value[2] if len(value) >= 3 else 1.0
        height = value[3] if len(value) >= 4 else 1.0
        unit = value[4] if len(value) >= 5 else TransformUnit.RATIO
        return cls(x=x, y=y, width=width, height=height, unit=unit)

    def calc(self, size: Tuple[float, float]):
        if self.unit == TransformUnit.ABSOLUTE:
            return self.x, self.y, self.width, self.height
        else:
            assert self.unit == TransformUnit.RATIO
            return (
                self.x * size[0],
                self.y * size[1],
                self.width * size[0],
                self.height * size[1],
            )

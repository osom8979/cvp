# -*- coding: utf-8 -*-

from typing import NamedTuple

import imgui


class SliderFloatResult(NamedTuple):
    clicked: bool
    value: float

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        clicked = result[0]
        value = result[1]
        assert isinstance(clicked, bool)
        assert isinstance(value, float)
        return cls(clicked, value)

    def __bool__(self):
        return self.clicked


def slider_float(
    label: str,
    value: float,
    min_value: float,
    max_value: float,
    fmt="%.3f",
    flags=0,
    power=1.0,
):
    result = imgui.slider_float(label, value, min_value, max_value, fmt, flags, power)
    return SliderFloatResult.from_raw(result)

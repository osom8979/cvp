# -*- coding: utf-8 -*-

from math import sqrt
from typing import List, Tuple

from cvp.types.shapes import Point


def create_dotted_line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    dot_length: float,
    space_length: float,
) -> List[Tuple[Point, Point]]:
    dx = x2 - x1
    dy = y2 - y1
    length = sqrt(dx**2 + dy**2)
    assert 0 <= length

    if length == 0:
        return list()

    if length <= dot_length:
        return [((x1, y1), (x2, y2))]

    result = list()
    current_length = 0.0
    direction_x = dx / length
    direction_y = dy / length

    while current_length < length:
        next_length = min(current_length + dot_length, length)
        start_x = x1 + direction_x * current_length
        start_y = y1 + direction_y * current_length
        end_x = x1 + direction_x * next_length
        end_y = y1 + direction_y * next_length
        result.append(((start_x, start_y), (end_x, end_y)))
        current_length += dot_length + space_length

    return result

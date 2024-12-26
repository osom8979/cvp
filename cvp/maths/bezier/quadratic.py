# -*- coding: utf-8 -*-

from typing import List

from cvp.types.shapes import Point


def calc_bezier_quadratic(p1: Point, p2: Point, p3: Point, t: float) -> Point:
    u = 1.0 - t
    w1 = u * u
    w2 = 2 * u * t
    w3 = t * t

    px = w1 * p1[0] + w2 * p2[0] + w3 * p3[0]
    py = w1 * p1[1] + w2 * p2[1] + w3 * p3[1]
    return px, py


def bezier_quadratic_points(
    p1: Point,
    p2: Point,
    p3: Point,
    num_segments: int,
) -> List[Point]:
    if num_segments <= 0:
        raise ValueError("The 'num_segments' argument must be greater than 0")

    result = [p1]
    t_step = 1.0 / num_segments
    for i_step in range(1, num_segments + 1):
        result.append(calc_bezier_quadratic(p1, p2, p3, t_step * i_step))
    return result

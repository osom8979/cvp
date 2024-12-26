# -*- coding: utf-8 -*-

from math import atan, cos
from math import degrees as math_degrees
from math import pi, sin, sqrt, tan
from typing import Optional, Tuple

from cvp.maths.equation.linear.errors import ParallelError
from cvp.types.shapes import Point, Rect


class GeneralForm:
    """
    General Form of Equation of a Line

    Ax + By + C = 0
    """

    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def from_coords(cls, x1: float, y1: float, x2: float, y2: float):
        """
        (y1 - y2)x + (x2 - x1)y + (x1y2 - x2y1) = 0
        """
        a = y1 - y2
        b = x2 - x1
        c = (x1 * y2) - (x2 * y1)
        return cls(a, b, c)

    @classmethod
    def from_points(cls, p1: Point, p2: Point):
        return cls.from_coords(p1[0], p1[1], p2[0], p2[1])

    @classmethod
    def from_coord_polar(cls, x1: float, y1: float, radians: float):
        """
        m = tan(radians)
        y - y1 = m (x - x1)
        y = mx - mx1 + y1
        0 = mx - mx1 + y1 - y
        0 = mx - y + (-mx1 + y1)
        A = m
        B = -1
        C = -m * x1 + y1
        """
        m = tan(radians)
        a = m
        b = -1
        c = -m * x1 + y1
        return cls(a, b, c)

    @classmethod
    def from_point_polar(cls, p1: Point, radians: float):
        return cls.from_coord_polar(p1[0], p1[1], radians)

    @classmethod
    def from_distance_polar(cls, distance: float, radians: float):
        x = distance * cos(radians)
        y = distance * sin(radians)
        return cls.from_coord_polar(x, y, radians + pi / 2)

    @classmethod
    def from_coord_degrees_polar(cls, x1: float, y1: float, degrees: float):
        """
        radians = degrees / 180 * pi
        """
        return cls.from_coord_polar(x1, y1, degrees / 180 * pi)

    @classmethod
    def from_point_degrees_polar(cls, p1: Point, degrees: float):
        """
        radians = degrees / 180 * pi
        """
        return cls.from_coord_polar(p1[0], p1[1], degrees / 180 * pi)

    def valid_coord(self, x: float, y: float) -> bool:
        return self.a * x + self.b * y + self.c == 0

    def valid_point(self, point: Point) -> bool:
        return self.valid_coord(point[0], point[1])

    def calc_x(self, y: float) -> float:
        """
        Ax + By + C = 0
        Ax = -By -C
        Ax = -(By + C)
        x = -(By + C) / A
        """
        return -1 * ((self.b * y) + self.c) / self.a

    def calc_y(self, x: float) -> float:
        """
        Ax + By + C = 0
        By = -Ax -C
        By = -(Ax + C)
        y = -(Ax + C) / B
        """
        return -1 * ((self.a * x) + self.c) / self.b

    @property
    def slope(self) -> float:
        """
        Slope of linear equation
        """
        return -1 * (self.a / self.b)

    @property
    def radians(self) -> float:
        return atan(self.slope)

    @property
    def degrees(self) -> float:
        return math_degrees(self.radians)

    @property
    def unsigned_radians(self) -> float:
        theta = self.radians
        assert -pi <= theta <= pi

        result = theta if theta >= 0 else 2 * pi + theta
        assert 0 <= result < 2 * pi
        return result

    @property
    def unsigned_degrees(self) -> float:
        return math_degrees(self.unsigned_radians)

    @property
    def vertical_slope(self) -> float:
        """
        vertical_slope * slope = -1
        vertical_slope = -1 / slope
        vertical_slope = -1 / (-1 * (self.a / self.b))
        vertical_slope = -1 * -1 * (self.b / self.a)
        vertical_slope = self.b / self.a
        """
        return self.b / self.a

    @property
    def vertical_radians(self) -> float:
        return atan(self.vertical_slope)

    @property
    def vertical_degrees(self) -> float:
        return math_degrees(self.vertical_radians)

    def create_vertical_form(self, x3: float, y3: float):
        return type(self).from_coord_polar(x3, y3, self.vertical_radians)

    def _get_left_point(self, left: float) -> Optional[Point]:
        if self.b == 0:
            return None
        return left, self.calc_y(left)

    def _get_top_point(self, top: float) -> Optional[Point]:
        if self.a == 0:
            return None
        return self.calc_x(top), top

    def _get_right_point(self, right: float) -> Optional[Point]:
        if self.b == 0:
            return None
        return right, self.calc_y(right)

    def _get_bottom_point(self, bottom: float) -> Optional[Point]:
        if self.a == 0:
            return None
        return self.calc_x(bottom), bottom

    def get_roi_points(self, roi: Rect) -> Tuple[Point, Point]:
        x1, y1, x2, y2 = roi
        left = min(x1, x2)
        right = max(x1, x2)
        top = min(y1, y2)
        bottom = max(y1, y2)

        lp = self._get_left_point(left)
        tp = self._get_top_point(top)
        rp = self._get_right_point(right)
        bp = self._get_bottom_point(bottom)

        points = set()
        if lp is not None and top <= lp[1] <= bottom:
            points.add(lp)
        if tp is not None and left <= tp[0] <= right:
            points.add(tp)
        if rp is not None and top <= rp[1] <= bottom:
            points.add(rp)
        if bp is not None and left <= bp[0] <= right:
            points.add(bp)

        if not points:
            raise IndexError("Out of canvas range error")

        assert len(points) in (1, 2)

        if len(points) == 1:
            p0 = points.pop()
            return p0, p0
        else:
            assert len(points) == 2
            p1 = points.pop()
            p2 = points.pop()
            return p1, p2

    def intersection(self, other: "GeneralForm") -> Point:
        """
        Ax + By + C = 0
        Dx + Ey + F = 0
        x = (CE - BF) / (BD - AE)
        y = (CD - AF) / (AE - BD)
        """

        a = self.a
        b = self.b
        c = self.c

        d = other.a
        e = other.b
        f = other.c

        x_numerator = c * e - b * f
        x_denominator = b * d - a * e

        y_numerator = c * d - a * f
        y_denominator = a * e - b * d

        if x_denominator == 0 or y_denominator == 0:
            raise ParallelError("Two straight lines are parallel or coincident")

        return x_numerator / x_denominator, y_numerator / y_denominator

    def distance_to_coord(self, x: float, y: float) -> float:
        """
        d = |ax + by + c| / sqrt(a^2 + b^2)
        """
        return abs(x * self.a + y * self.b + self.c) / sqrt(self.a**2 + self.b**2)

    def distance_to_point(self, point: Point) -> float:
        return self.distance_to_coord(point[0], point[1])

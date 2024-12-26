# -*- coding: utf-8 -*-


class SlopeInterceptForm:
    """
    Equation of a Straight Line

    y = mx + b
    """

    def __init__(self, m: float, b: float):
        self.m = m
        self.b = b

    def calc_y(self, x: float) -> float:
        return self.m * x + self.b

    def calc_x(self, y: float) -> float:
        """
        y = mx + b
        y - b = mx
        (y - b) / m = x
        """
        return (y - self.b) / self.m

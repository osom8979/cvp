# -*- coding: utf-8 -*-


class PointSlopeForm:
    """
    Point-Slope Equation of a Line

    y − y1 = m(x − x1)
    """

    def __init__(self, x1: float, y1: float, m: float):
        self.x1 = x1
        self.y1 = y1
        self.m = m

    def calc_y(self, x: float) -> float:
        """
        y − y1 = m(x − x1)
        y = m(x − x1) + y1
        """
        return self.m * (x - self.x1) + self.y1

    def calc_x(self, y: float) -> float:
        """
        y − y1 = m(x − x1)
        (y − y1) / m = x − x1
        (y − y1) / m + x1 = x
        """
        return (y - self.y1) / self.m + self.y1

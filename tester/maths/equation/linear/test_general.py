# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.maths.equation.linear.general import GeneralForm


def find_x3_given_line_through_points(x1, y1, x2, y2, y3):
    """
    Find x3 on the two lines passing through the given points.
    """
    slope = (y2 - y1) / (x2 - x1)
    return x1 + (y3 - y1) / slope


class LinearTestCase(TestCase):
    def test_find_x3_given_line_through_points(self):
        x1, y1 = 1, 1
        x2, y2 = 2, 3
        x3, y3 = 3, 5
        self.assertEqual(x3, find_x3_given_line_through_points(x1, y1, x2, y2, y3))

    def test_general_form(self):
        x1, y1 = 1, 1
        x2, y2 = 2, 3
        x3, y3 = 3, 5
        form = GeneralForm.from_coords(x1, y1, x2, y2)
        self.assertEqual(x3, form.calc_x(y3))
        self.assertEqual(y3, form.calc_y(x3))


if __name__ == "__main__":
    main()

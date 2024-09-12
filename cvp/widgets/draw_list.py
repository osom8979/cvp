# -*- coding: utf-8 -*-

import imgui
from imgui.core import _DrawList  # noqa


def get_window_draw_list():
    draw_list = imgui.get_window_draw_list()
    assert isinstance(draw_list, _DrawList)
    return draw_list

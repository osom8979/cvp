# -*- coding: utf-8 -*-

import imgui

# noinspection PyProtectedMember
from imgui.core import _DrawList as DrawList


def create_empty_draw_list():
    return DrawList()


def get_window_draw_list():
    draw_list = imgui.get_window_draw_list()
    assert isinstance(draw_list, DrawList)
    return draw_list


def get_foreground_draw_list():
    draw_list = imgui.get_foreground_draw_list()
    assert isinstance(draw_list, DrawList)
    return draw_list

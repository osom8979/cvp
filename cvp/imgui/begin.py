# -*- coding: utf-8 -*-

import imgui


def begin(label: str, closable=False, flags=0):
    return imgui.begin(label, closable, flags)


def end() -> None:
    imgui.end()

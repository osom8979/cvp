# -*- coding: utf-8 -*-

from dataclasses import dataclass

import imgui


@dataclass
class WindowQuery:
    x: float = 0.0
    y: float = 0.0
    w: float = 0.0
    h: float = 0.0

    def update(self):
        self.x, self.y = imgui.get_window_position()
        self.w, self.h = imgui.get_window_size()

    @property
    def position(self):
        return self.x, self.y

    @property
    def size(self):
        return self.w, self.h

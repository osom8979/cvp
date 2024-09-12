# -*- coding: utf-8 -*-

import imgui


class ControlTab:
    def __init__(self):
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 1.0
        self.zoom_step = 0.02
        self.zoom_min = 0.01
        self.zoom_max = 10.0
        self.alpha = 1.0

    def _main(self):
        imgui.text("View")
        self.pan_x, self.pan_y = imgui.drag_float2(
            "Pan", self.pan_x, self.pan_y, 0.1, 0.0, 0.0, "%.1f"
        )[1]
        self.zoom = imgui.slider_float(
            "Zoom", self.zoom, self.zoom_min, self.zoom_max, "%.2f"
        )[1]
        self.alpha = imgui.slider_float("Alpha", self.alpha, 0.0, 1.0, "%.3f")[1]

        if imgui.button("Reset"):
            self.pan_x = 0.0
            self.pan_y = 0.0
            self.zoom = 1.0
            self.alpha = 1.0

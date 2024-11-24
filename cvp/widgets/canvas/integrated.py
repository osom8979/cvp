# -*- coding: utf-8 -*-

from typing import Optional

from cvp.flow.datas import Canvas as CanvasProps
from cvp.renderer.widget.interface import WidgetInterface
from cvp.types.override import override
from cvp.widgets.canvas._base import BaseCanvas


class IntegratedCanvas(BaseCanvas, WidgetInterface):
    def __init__(self, canvas_props: Optional[CanvasProps] = None):
        super().__init__(canvas_props)

    @override
    def on_process(self) -> None:
        self.next_state()
        assert self._draw_list is not None
        self.do_button_control()
        # draw_list = self._draw_list
        # mx, my = self._mouse_pos
        # cx, cy = self._canvas_pos
        # cw, ch = self._canvas_size
        # hovering = self._hovering
        # left_button = self._left_button_clicked
        # middle_button = self._middle_button_clicked
        # right_button = self._right_button_clicked

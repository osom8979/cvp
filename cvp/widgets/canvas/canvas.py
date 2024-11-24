# -*- coding: utf-8 -*-

from cvp.renderer.widget.interface import WidgetInterface
from cvp.types.override import override


class Canvas(WidgetInterface):
    def __init__(self):
        pass

    @override
    def on_process(self) -> None:
        pass

# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

import imgui

from cvp.variables import MIN_OPEN_FILE_POPUP_HEIGHT, MIN_OPEN_FILE_POPUP_WIDTH
from cvp.widgets.set_window_min_size import set_window_min_size

ResultT = TypeVar("ResultT")


class Popup(Generic[ResultT], ABC):
    _result: Optional[ResultT]

    def __init__(
        self,
        title: Optional[str] = None,
        centered=True,
        flags=0,
        min_width=MIN_OPEN_FILE_POPUP_WIDTH,
        min_height=MIN_OPEN_FILE_POPUP_HEIGHT,
    ):
        self._title = title if title else type(self).__name__

        self._visible = False
        self._centered = centered
        self._flags = flags

        self._min_width = min_width
        self._min_height = min_height

        self._result = None

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value: Optional[ResultT]) -> None:
        self._result = value

    def show(self) -> None:
        self._visible = True

    def process(self) -> Optional[ResultT]:
        if self._visible:
            imgui.open_popup(self._title)
            self._visible = False

        if self._centered:
            x, y = imgui.get_main_viewport().get_center()
            px, py = 0.5, 0.5
            imgui.set_next_window_position(x, y, imgui.APPEARING, px, py)

        modal = imgui.begin_popup_modal(self._title, None, self._flags)  # noqa
        if not modal.opened:
            self._result = None
            return None

        if imgui.is_window_appearing():
            set_window_min_size(self._min_width, self._min_height)

        try:
            self._result = self._main()
            return self._result
        finally:
            imgui.end_popup()

    @abstractmethod
    def _main(self) -> Optional[ResultT]:
        raise NotImplementedError

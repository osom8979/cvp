# -*- coding: utf-8 -*-

from typing import Callable, Optional

import imgui
import pygame

from cvp.widgets.button_ex import button_ex

ENTER_RETURN = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE


class OpenUrlPopup:
    _result: Optional[str]
    _callback: Optional[Callable[[str], None]]

    def __init__(self):
        self._enabled = False
        self._title = str()
        self._url = str()
        self._result = None
        self._callback = None
        self._centered = True
        self._min_width = 400
        self._min_height = 140

    def show(
        self,
        title: Optional[str] = None,
        callback: Optional[Callable[[str], None]] = None,
        centered=True,
    ) -> None:
        self._enabled = True
        self._title = title if title else type(self).__name__
        self._result = None
        self._callback = callback
        self._centered = centered

    def _close(self, url: Optional[str] = None) -> None:
        self._result = url
        if self._callback:
            self._callback(url if url else str())
        imgui.close_current_popup()

    def _main(self) -> None:
        if imgui.is_window_appearing():
            imgui.set_window_size(self._min_width, self._min_height)

        imgui.text("Please enter a network URL:")

        if imgui.is_window_appearing():
            imgui.set_keyboard_focus_here()

        window_width = imgui.get_content_region_available_width()
        imgui.push_item_width(window_width)
        self._url = imgui.input_text("#URL", self._url, -1, ENTER_RETURN)[1]
        imgui.pop_item_width()

        if button_ex("Open", disabled=not self._url):
            self._close(self._url)

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            self._close(self._url)

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self._close()

    def process(self) -> None:
        if self._enabled:
            imgui.open_popup(self._title)
            self._enabled = False

        if self._centered:
            x, y = imgui.get_main_viewport().get_center()
            px, py = 0.5, 0.5
            imgui.set_next_window_position(x, y, imgui.APPEARING, px, py)

        modal = imgui.begin_popup_modal(self._title)
        if not modal.opened:
            return

        try:
            self._main()
        finally:
            imgui.end_popup()

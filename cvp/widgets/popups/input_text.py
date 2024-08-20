# -*- coding: utf-8 -*-

from typing import Optional

import imgui
import pygame

from cvp.variables import MIN_OPEN_URL_POPUP_HEIGHT, MIN_OPEN_URL_POPUP_WIDTH
from cvp.widgets.button_ex import button_ex
from cvp.widgets.input_text_value import input_text_value
from cvp.widgets.item_width import item_width
from cvp.widgets.set_window_min_size import set_window_min_size


class InputTextPopup:
    def __init__(
        self,
        title: Optional[str] = None,
        label: Optional[str] = None,
        text: Optional[str] = None,
        ok: Optional[str] = None,
        cancel: Optional[str] = None,
        centered=True,
    ):
        self._title = title if title else type(self).__name__
        self._label = label if label else str()
        self._text = text if text else str()
        self._ok_button_label = ok if ok else "Ok"
        self._cancel_button_label = cancel if cancel else "Cancel"
        self._text_label = "## Text"
        self._centered = centered

        self._enabled = False
        self._min_width = MIN_OPEN_URL_POPUP_WIDTH
        self._min_height = MIN_OPEN_URL_POPUP_HEIGHT

    @property
    def text(self):
        return self._text

    def show(self) -> None:
        self._enabled = True

    def process(self) -> Optional[str]:
        if self._enabled:
            imgui.open_popup(self._title)
            self._enabled = False

        if self._centered:
            x, y = imgui.get_main_viewport().get_center()
            px, py = 0.5, 0.5
            imgui.set_next_window_position(x, y, imgui.APPEARING, px, py)

        modal = imgui.begin_popup_modal(self._title)
        if not modal.opened:
            return None

        try:
            return self._main()
        finally:
            imgui.end_popup()

    def _main(self) -> Optional[str]:
        if imgui.is_window_appearing():
            set_window_min_size(self._min_width, self._min_height)

        if self._label:
            imgui.text(self._label)

        if imgui.is_window_appearing():
            imgui.set_keyboard_focus_here()

        with item_width(-1):
            self._text = input_text_value(self._text_label, self._text)

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            imgui.close_current_popup()
            return self._text
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            imgui.close_current_popup()
            return None

        if button_ex(self._cancel_button_label):
            imgui.close_current_popup()
            return None
        imgui.same_line()
        if button_ex(self._ok_button_label, disabled=not self._text):
            imgui.close_current_popup()
            return self._text

        return None

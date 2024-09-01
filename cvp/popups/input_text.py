# -*- coding: utf-8 -*-

from typing import Optional

import imgui
import pygame

from cvp.types import override
from cvp.widgets import button_ex, input_text_value, item_width
from cvp.widgets.hoc.popup import Popup


class InputTextPopup(Popup[str]):
    def __init__(
        self,
        title: Optional[str] = None,
        label: Optional[str] = None,
        text: Optional[str] = None,
        ok: Optional[str] = None,
        cancel: Optional[str] = None,
        centered=True,
        flags=0,
    ):
        super().__init__(title, centered, flags)
        self._label = label if label else str()
        self._text = text if text else str()
        self._ok_button_label = ok if ok else "Ok"
        self._cancel_button_label = cancel if cancel else "Cancel"
        self._text_label = "## Text"

    @property
    def text(self):
        return self._text

    @override
    def on_process(self) -> Optional[str]:
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

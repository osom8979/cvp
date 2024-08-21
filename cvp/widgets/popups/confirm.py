# -*- coding: utf-8 -*-

from typing import Optional

import imgui
import pygame

from cvp.types.override import override
from cvp.widgets.button_ex import button_ex
from cvp.widgets.popups._popup import Popup


class ConfirmPopup(Popup[bool]):
    def __init__(
        self,
        title: Optional[str] = None,
        label: Optional[str] = None,
        ok: Optional[str] = None,
        cancel: Optional[str] = None,
        centered=True,
        flags=0,
    ):
        super().__init__(title, centered, flags)
        self._label = label if label else str()
        self._ok_button_label = ok if ok else "Ok"
        self._cancel_button_label = cancel if cancel else "Cancel"

    @override
    def on_process(self) -> Optional[bool]:
        if self._label:
            imgui.text(self._label)

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            imgui.close_current_popup()
            return True
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            imgui.close_current_popup()
            return False

        if button_ex(self._cancel_button_label):
            imgui.close_current_popup()
            return False
        imgui.same_line()
        if button_ex(self._ok_button_label):
            imgui.close_current_popup()
            return True

        return None

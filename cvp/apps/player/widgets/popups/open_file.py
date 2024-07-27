# -*- coding: utf-8 -*-

import os
from os import PathLike
from pathlib import Path
from typing import Callable, List, Optional, Union

import imgui
import pygame

from cvp.apps.player.widgets.button_ex import button_ex
from cvp.logging.logging import logger

ENTER_RETURN = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
ALLOW_DOUBLE_CLICK = imgui.SELECTABLE_ALLOW_DOUBLE_CLICK


class OpenFilePopup:
    _items: List[str]
    _result: Optional[str]
    _callback: Optional[Callable[[str], None]]

    def __init__(self, title="Open file"):
        self._default_title = title
        self._enabled = False
        self._title = title
        self._location_text = str()
        self._current_dir = str()
        self._items = list()
        self._selected = str()
        self._result = None
        self._callback = None
        self._centered = True
        self._show_hidden = False

    @staticmethod
    def list_items(location: Union[str, PathLike], show_hidden=False) -> List[str]:
        dirs = list()
        files = list()

        items = os.listdir(location)
        items.sort()

        for item in items:
            if not show_hidden and item.startswith("."):
                continue
            item_path = os.path.join(location, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            elif os.path.isfile(item_path):
                files.append(item)

        return dirs + files

    def show(
        self,
        title: Optional[str] = None,
        directory: Optional[Union[str, PathLike]] = None,
        callback: Optional[Callable[[str], None]] = None,
        centered=True,
        show_hidden=False,
    ) -> None:
        if isinstance(directory, Path) and directory.is_dir():
            dir_path = directory
        elif isinstance(directory, str) and os.path.isdir(directory):
            dir_path = Path(directory)
        else:
            dir_path = Path.home()

        self._enabled = True
        self._title = title if title else self._default_title
        self._location_text = str(dir_path)
        self._current_dir = str()
        self._items = list()
        self._selected = str()
        self._result = None
        self._callback = callback
        self._centered = centered
        self._show_hidden = show_hidden

    def _close(self, path: Optional[str] = None) -> None:
        self._result = path
        if self._callback:
            self._callback(path if path else str())
        imgui.close_current_popup()

    def _main(self) -> None:
        if imgui.button("Parent"):
            self._location_text = str(Path(self._location_text).parent)

        imgui.same_line()

        loc_text = self._location_text
        loc_changed, loc_text = imgui.input_text("Location", loc_text, -1, ENTER_RETURN)

        if loc_changed:
            if os.path.isfile(loc_text):
                self._close(loc_text)
            elif os.path.isdir(loc_text):
                self._location_text = loc_text
            else:
                logger.warning(f"Invalid location: '{loc_text}'")

        imgui.same_line()

        if imgui.checkbox("Show Hidden", self._show_hidden)[0]:
            self._show_hidden = not self._show_hidden
            self._items = self.list_items(self._current_dir, self._show_hidden)

        item_spacing_y = imgui.get_style().item_spacing.y
        frame_height_with_spacing = imgui.get_frame_height_with_spacing()
        footer_height_to_reserve = item_spacing_y + frame_height_with_spacing
        remain_height = -footer_height_to_reserve

        if imgui.begin_child("Files", 0, remain_height, border=True):  # noqa
            if self._current_dir != self._location_text:
                # Update items
                self._current_dir = self._location_text
                self._selected = str()
                self._items = self.list_items(self._current_dir, self._show_hidden)

            for item in self._items:
                item_path = os.path.join(self._location_text, item)
                selected = item_path == self._selected

                if os.path.isfile(item_path):
                    if imgui.selectable(item, selected, ALLOW_DOUBLE_CLICK)[0]:
                        self._selected = item_path
                        if imgui.is_mouse_double_clicked(0):
                            self._close(item_path)
                elif os.path.isdir(item_path):
                    if imgui.selectable(item + "/", selected, ALLOW_DOUBLE_CLICK)[0]:
                        self._selected = item_path
                        if imgui.is_mouse_double_clicked(0):
                            self._location_text = item_path

            imgui.end_child()

        imgui.separator()

        select_file = os.path.isfile(self._selected)
        select_dir = os.path.isdir(self._selected)
        enabled_open = select_file or select_dir

        if button_ex("Open", disabled=not enabled_open):
            if select_file:
                self._close(self._selected)
            elif select_dir:
                self._location_text = self._selected

        imgui.same_line()

        if imgui.button("Close"):
            self._close()

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self._close()

        if self._selected and pygame.key.get_pressed()[pygame.K_RETURN]:
            if select_file:
                self._close(self._selected)
            elif select_dir:
                self._location_text = self._selected

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

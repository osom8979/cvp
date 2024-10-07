# -*- coding: utf-8 -*-

import os
from typing import Mapping

import imgui
from cvp.config.sections.media_window import MediaWindowSection
from cvp.config.sections.media_window import Mode as MediaSectionMode
from cvp.config.sections.medias import MediasSection
from cvp.context import Context
from cvp.imgui.button_ex import button_ex
from cvp.popups.confirm import ConfirmPopup
from cvp.popups.input_text import InputTextPopup
from cvp.popups.open_file import OpenFilePopup
from cvp.types import override
from cvp.widgets.manager_tab import ManagerTab
from cvp.widgets.window_mapper import WindowMapper
from cvp.windows.media.info import MediaInfoTab
from cvp.windows.media.media import MediaWindow


class MediaManager(ManagerTab[MediasSection, MediaWindowSection]):
    def __init__(self, context: Context, windows: WindowMapper):
        super().__init__(
            context=context,
            section=context.config.media_manager,
            title="Media Manager",
            closable=True,
            flags=None,
        )
        self._windows = windows
        self.register(MediaInfoTab(context))

        self._open_file_popup = OpenFilePopup(
            title="Open file",
            target=self.on_open_file_popup,
        )
        self._open_url_popup = InputTextPopup(
            title="Open network stream",
            label="Please enter a network URL:",
            ok="Open",
            cancel="Close",
            target=self.on_open_url_popup,
        )
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove media?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )

        self.register_popup(self._open_file_popup)
        self.register_popup(self._open_url_popup)
        self.register_popup(self._confirm_remove)

    def add_media_window(self, section: MediaWindowSection) -> None:
        window = MediaWindow(self._context, section)
        self._windows.add_window(window, window.key)

    def add_media_windows(self, *sections: MediaWindowSection) -> None:
        for section in sections:
            self.add_media_window(section)

    def open_media(self, file: str, mode: MediaSectionMode) -> None:
        section = self.context.config.add_media_section()
        section.opened = True
        section.file = file
        section.mode = mode
        if mode == MediaSectionMode.file:
            section.title = os.path.basename(file)
        else:
            section.title = file
        self.add_media_window(section)

    def close_media(self, key: str) -> None:
        self._windows.pop_window(key)
        self.context.config.remove_section(key)

    @override
    def on_create(self) -> None:
        self.add_media_windows(*self.context.config.media_sections.values())

    @override
    def on_process_sidebar_top(self) -> None:
        if imgui.button("File"):
            self._open_file_popup.show()
        imgui.same_line()
        if imgui.button("URL"):
            self._open_url_popup.show()
        imgui.same_line()
        selected_menu = self.latest_menus.get(self.selected)
        if button_ex("Remove", disabled=selected_menu is None):
            self._confirm_remove.show()

    @override
    def get_menus(self) -> Mapping[str, MediaWindowSection]:
        return self._context.config.media_sections

    def on_open_file_popup(self, file: str) -> None:
        self.open_media(file, MediaSectionMode.file)

    def on_open_url_popup(self, url: str) -> None:
        self.open_media(url, MediaSectionMode.url)

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return

        selected_menu = self.latest_menus.get(self.selected)
        assert selected_menu is not None

        self.close_media(selected_menu.section)

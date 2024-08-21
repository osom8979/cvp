# -*- coding: utf-8 -*-

import imgui

from cvp.config.config import Config
from cvp.config.sections.media import MediaSection
from cvp.ffmpeg.ffmpeg.manager import FFmpegManager
from cvp.ffmpeg.ffprobe.inspect import inspect_video_frame_size
from cvp.variables import MIN_SIDEBAR_WIDTH, MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets import (
    button_ex,
    footer_height_to_reserve,
    input_text_disabled,
    input_text_value,
    item_width,
    set_window_min_size,
    text_centered,
)


class ManagerWindow:
    def __init__(self, ffmpegs: FFmpegManager, config: Config):
        self._ffmpegs = ffmpegs
        self._config = config
        self._title = "Media Manger"
        self._flags = 0
        self._min_width = MIN_WINDOW_WIDTH
        self._min_height = MIN_WINDOW_HEIGHT
        self._min_sidebar_width = MIN_SIDEBAR_WIDTH

    @property
    def opened(self) -> bool:
        return self._config.manager.opened

    @opened.setter
    def opened(self, value: bool) -> None:
        self._config.manager.opened = value

    @property
    def sidebar_width(self) -> int:
        return self._config.manager.sidebar_width

    @sidebar_width.setter
    def sidebar_width(self, value: int) -> None:
        self._config.manager.sidebar_width = value

    @property
    def selected(self) -> str:
        return self._config.manager.selected

    @selected.setter
    def selected(self, value: str) -> None:
        self._config.manager.selected = value

    @property
    def medias(self):
        return self._config.medias

    def drag_sidebar_width(self):
        sidebar_width = imgui.drag_int(
            "## SideWidth",
            self.sidebar_width,
            1.0,
            self._min_sidebar_width,
            0,
            "Sidebar Width %d",
        )[1]
        if sidebar_width < self._min_sidebar_width:
            sidebar_width = self._min_sidebar_width
        self.sidebar_width = sidebar_width

    def process(self) -> None:
        if not self.opened:
            return

        expanded, opened = imgui.begin(self._title, True, self._flags)
        try:
            if not opened:
                self.opened = False
                return

            if not expanded:
                return

            self._main()
        finally:
            imgui.end()

    def _main(self) -> None:
        if imgui.is_window_appearing():
            set_window_min_size(self._min_width, self._min_height)

        medias = self._config.medias
        media = medias.get(self.selected, None)

        # noinspection PyArgumentList
        imgui.begin_child("## Sidebar", self.sidebar_width, 0, border=True)
        try:
            imgui.text("Medias")

            content_width = imgui.get_content_region_available_width()
            imgui.set_next_item_width(content_width)
            self.drag_sidebar_width()

            imgui.separator()

            menus = imgui.begin_list_box("## SideList", width=-1, height=-1)
            if menus.opened:
                for key, section in medias.items():
                    if imgui.selectable(section.name, key == self.selected)[1]:
                        self.selected = key
                imgui.end_list_box()
        finally:
            imgui.end_child()

        imgui.same_line()

        # noinspection PyArgumentList
        imgui.begin_child("## Main", -1, -footer_height_to_reserve())
        try:
            if media is not None:
                self._media_tab_bar(media)
            else:
                text_centered("Please select a media item")
        finally:
            imgui.end_child()

    def _media_tab_bar(self, media: MediaSection) -> None:
        if not imgui.begin_tab_bar("Media Tabs"):
            return

        try:
            self._basic_tab(media)
        finally:
            imgui.end_tab_bar()

    def _basic_tab(self, media: MediaSection) -> None:
        if not imgui.begin_tab_item("Basic").selected:
            return

        try:
            imgui.text("Section:")
            input_text_disabled("## Section", media.section)

            imgui.text("Name:")
            with item_width(-1):
                media.name = input_text_value("## Name", media.name)

            imgui.text("File:")
            with item_width(-1):
                media.file = input_text_value("## File", media.file)

            key = media.section
            spawnable = self._ffmpegs.spawnable(key)
            stoppable = self._ffmpegs.stoppable(key)
            removable = self._ffmpegs.removable(key)

            imgui.separator()
            imgui.text("Frame:")
            media.frame_size = imgui.input_int2("Size", *media.frame_size)[1]
            if imgui.button("Reset"):
                media.frame_size = 0, 0
            imgui.same_line()
            if imgui.button("Inspect"):
                try:
                    media.frame_size = inspect_video_frame_size(media.file)
                except BaseException as e:
                    print(e)

            imgui.separator()
            try:
                status = self._ffmpegs.status(key)
            except BaseException as e:
                status = str(e)
            imgui.text(f"Process ({status})")

            if button_ex("Spawn", disabled=not spawnable):
                self._ffmpegs.spawn_with_file(
                    key,
                    media.frame_width,
                    media.frame_height,
                    media.file,
                )
                pass
            imgui.same_line()
            if button_ex("Stop", disabled=not stoppable):
                self._ffmpegs.interrupt(key)
            imgui.same_line()
            if button_ex("Remove", disabled=not removable):
                self._ffmpegs.pop(key)
        finally:
            imgui.end_tab_item()

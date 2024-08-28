# -*- coding: utf-8 -*-

import imgui

from cvp.config.config import Config
from cvp.config.sections.manager import ManagerSection
from cvp.config.sections.media import MediaSection
from cvp.ffmpeg.ffprobe.inspect import inspect_video_frame_size
from cvp.process.manager import ProcessManager
from cvp.types.override import override
from cvp.variables import MIN_SIDEBAR_WIDTH
from cvp.widgets import (
    begin_child,
    button_ex,
    end_child,
    footer_height_to_reserve,
    input_text_disabled,
    input_text_value,
    item_width,
    text_centered,
)
from cvp.widgets.hoc.window import Window


class ManagerWindow(Window[ManagerSection]):
    def __init__(self, pm: ProcessManager, config: Config):
        super().__init__(
            config.manager,
            title="Media Manager",
            closable=True,
        )
        self._pm = pm
        self._medias = config.medias
        self._min_sidebar_width = MIN_SIDEBAR_WIDTH

    @property
    def sidebar_width(self) -> int:
        return self.section.sidebar_width

    @sidebar_width.setter
    def sidebar_width(self, value: int) -> None:
        self.section.sidebar_width = value

    @property
    def selected(self) -> str:
        return self.section.selected

    @selected.setter
    def selected(self, value: str) -> None:
        self.section.selected = value

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

    @override
    def on_process(self) -> None:
        if begin_child("## Sidebar", self.sidebar_width, border=True).visible:
            try:
                content_width = imgui.get_content_region_available_width()
                imgui.set_next_item_width(content_width)
                self.drag_sidebar_width()

                imgui.separator()

                if imgui.begin_list_box("## SideList", width=-1, height=-1).opened:
                    for key, section in self._medias.items():
                        if imgui.selectable(section.name, key == self.selected)[1]:
                            self.selected = key
                    imgui.end_list_box()
            finally:
                end_child()

        imgui.same_line()

        if begin_child("## Main", -1, -footer_height_to_reserve()).visible:
            try:
                media = self._medias.get(self.selected, None)
                if media is not None:
                    self._media_tab_bar(media)
                else:
                    text_centered("Please select a media item")
            finally:
                end_child()

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

            spawnable = self._pm.spawnable(media.section)
            stoppable = self._pm.stoppable(media.section)
            removable = self._pm.removable(media.section)

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
                status = self._pm.status(media.section)
            except BaseException as e:
                status = str(e)
            imgui.text(f"Process ({status})")

            if button_ex("Spawn", disabled=not spawnable):
                self._pm.spawn_with_file(
                    media.section,
                    media.frame_width,
                    media.frame_height,
                    media.file,
                )
                pass
            imgui.same_line()
            if button_ex("Stop", disabled=not stoppable):
                self._pm.interrupt(media.section)
            imgui.same_line()
            if button_ex("Remove", disabled=not removable):
                self._pm.pop(media.section)
        finally:
            imgui.end_tab_item()

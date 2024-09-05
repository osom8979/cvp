# -*- coding: utf-8 -*-

import imgui

from cvp.config.sections.windows.medias import MediasSection
from cvp.context import Context
from cvp.types import override
from cvp.variables import MIN_SIDEBAR_WIDTH
from cvp.widgets import begin_child, end_child, text_centered
from cvp.widgets.hoc.window import Window
from cvp.windows.medias.tabs import MediaTabs


class MediasWindow(Window[MediasSection]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            section=context.config.medias,
            title="Medias",
            closable=True,
            flags=None,
        )

        self._min_sidebar_width = MIN_SIDEBAR_WIDTH
        self._tabs = MediaTabs(context)

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

    def drag_sidebar_width(self) -> None:
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
        media_sections = self.context.config.media_sections

        if begin_child("## Sidebar", self.sidebar_width, border=True).visible:
            try:
                content_width = imgui.get_content_region_available_width()
                imgui.set_next_item_width(content_width)
                self.drag_sidebar_width()

                imgui.separator()

                if imgui.begin_list_box("## SideList", width=-1, height=-1).opened:
                    for key, section in media_sections.items():
                        label = f"{section.title}##{key}"
                        if imgui.selectable(label, key == self.selected)[1]:
                            self.selected = key
                    imgui.end_list_box()
            finally:
                end_child()

        imgui.same_line()

        if begin_child("## Main", -1, -1).visible:
            try:
                media = media_sections.get(self.selected, None)
                if media is not None:
                    self._tabs.do_process(media)
                else:
                    text_centered("Please select a media item")
            finally:
                end_child()

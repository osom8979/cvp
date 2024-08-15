# -*- coding: utf-8 -*-

import imgui

from cvp.config.config import Config
from cvp.process.manager import ProcessManager
from cvp.variables import MIN_SIDEBAR_WIDTH, MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets.button_ex import button_ex

ENTER_RETURN = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
READ_ONLY = imgui.INPUT_TEXT_READ_ONLY


class ManagerWindow:
    def __init__(self, processes: ProcessManager, config: Config):
        self._processes = processes
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

    def process(self) -> None:
        self._process_window()

    def _process_window(self) -> None:
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

    def _main(self) -> None:
        if imgui.is_window_appearing():
            cw, ch = imgui.get_window_size()
            w = cw if cw >= self._min_width else self._min_width
            h = ch if ch >= self._min_height else self._min_height
            imgui.set_window_size(w, h)

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

        # Reserve enough left-over height for 1 separator + 1 input text
        footer_height_to_reserve = (
            imgui.get_frame_height_with_spacing() + imgui.get_style().item_spacing.y
        )

        # noinspection PyArgumentList
        imgui.begin_child("## Main", -1, -footer_height_to_reserve)
        try:
            if media is not None:
                if imgui.begin_tab_bar("Media Tabs"):
                    if imgui.begin_tab_item("Info").selected:
                        imgui.text("Section:")
                        imgui.push_item_width(-1)
                        imgui.push_style_color(
                            imgui.COLOR_FRAME_BACKGROUND, 0.2, 0.2, 0.2
                        )
                        imgui.push_style_color(imgui.COLOR_TEXT, 0.8, 0.8, 0.8)
                        imgui.input_text("## Section", media.section, -1, READ_ONLY)
                        imgui.pop_style_color(2)
                        imgui.pop_item_width()

                        imgui.separator()

                        imgui.text("Name:")
                        imgui.push_item_width(-1)
                        media.name = imgui.input_text(
                            "## Name", media.name, -1, ENTER_RETURN
                        )[1]
                        imgui.pop_item_width()

                        imgui.separator()

                        imgui.text("File:")
                        imgui.push_item_width(-1)
                        media.file = imgui.input_text(
                            "## File", media.file, -1, ENTER_RETURN
                        )[1]
                        imgui.pop_item_width()

                        imgui.separator()

                        if button_ex("Start"):
                            # self._processes.spawn(
                            #     media.section,
                            #     (
                            #         "ffmpeg",
                            #         "-hide_banner",
                            #         "-fflags",
                            #         "nobuffer",
                            #         "-fflags",
                            #         "discardcorrupt",
                            #         "-flags",
                            #         "low_delay",
                            #         "-rtsp_transport",
                            #         "tcp",
                            #         "-i",
                            #         media.file,
                            #         "-f",
                            #         "image2pipe",
                            #         "-pix_fmt",
                            #         "rgb24",
                            #         "-vcodec",
                            #         "rawvideo",
                            #         "pipe:1",
                            #     ),
                            # )
                            pass
                        if button_ex("Stop"):
                            pass

                        imgui.end_tab_item()
                    imgui.end_tab_bar()
            else:
                message = "Please select a media item"
                window_size = imgui.get_window_size()
                text_size = imgui.calc_text_size(message)
                text_x = (window_size.x - text_size.x) * 0.5
                text_y = (window_size.y - text_size.y) * 0.5
                imgui.set_cursor_pos((text_x, text_y))
                imgui.text(message)
        finally:
            imgui.end_child()

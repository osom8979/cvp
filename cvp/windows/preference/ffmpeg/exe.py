# -*- coding: utf-8 -*-

from shutil import which
from typing import List, Optional, Sequence
from weakref import ref

import imgui

from cvp.config.proxy import ValueProxy
from cvp.config.sections.ffmpeg import FFmpegProxy, FFmpegSection, FFprobeProxy
from cvp.popups.open_file import OpenFilePopup
from cvp.process.manager import ProcessManager
from cvp.types import override
from cvp.widgets import button_ex, item_width
from cvp.widgets.hoc.popup import Popup, PopupPropagator
from cvp.widgets.hoc.tab import TabBar, TabItem


class ExeItem(TabItem, PopupPropagator):
    def __init__(self, filename: str, proxy: ValueProxy, pm: ProcessManager):
        super().__init__(filename)
        self._filename = filename
        self._proxy = proxy
        self._pm = ref(pm)
        self._browser = OpenFilePopup(
            f"Select {self._filename} executable",
            target=self.on_browser,
        )

    @property
    @override
    def popups(self) -> Sequence[Popup]:
        return [self._browser]

    @property
    def pm(self) -> Optional[ProcessManager]:
        return self._pm()

    @property
    def exe_path(self) -> str:
        return self._proxy.get()

    @exe_path.setter
    def exe_path(self, value: str) -> None:
        self._proxy.set(value)

    def on_browser(self, file: str) -> None:
        self.exe_path = file

    @override
    def on_process(self) -> None:
        imgui.text(f"{self._label} executable")

        with item_width(-1):
            path_result = imgui.input_text(
                f"##{self._label}Path",
                self.exe_path,
                imgui.INPUT_TEXT_ENTER_RETURNS_TRUE,
            )

        path_changed = path_result[0]
        if path_changed:
            path_value = path_result[1]
            assert isinstance(path_value, str)
            self.exe_path = path_value

        if imgui.button(f"Default##{self._label}Default"):
            self.exe_path = self._filename

        imgui.same_line()
        which_path = which(self._filename)
        if button_ex(f"Which##{self._label}Which", disabled=not which_path):
            assert isinstance(which_path, str)
            self.exe_path = which_path

        imgui.same_line()
        if button_ex(f"Cache##{self._label}Cache"):
            pass

        imgui.same_line()
        if button_ex(f"Browse##{self._label}Browse"):
            self._browser.show()


class ExeTabs(TabBar, PopupPropagator):
    def __init__(self, section: FFmpegSection, pm: ProcessManager):
        super().__init__()
        self.register(ExeItem("ffmpeg", FFmpegProxy(section), pm))
        self.register(ExeItem("ffprobe", FFprobeProxy(section), pm))

    @property
    @override
    def popups(self) -> Sequence[Popup]:
        result: List[Popup] = list()
        for item in self._items.values():
            if not isinstance(item, PopupPropagator):
                continue
            result.extend(item.popups)
        return result

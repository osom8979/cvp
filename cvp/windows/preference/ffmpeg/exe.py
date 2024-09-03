# -*- coding: utf-8 -*-

from shutil import which
from typing import List, Sequence

import imgui

from cvp.config.proxy import ValueProxy
from cvp.config.sections.ffmpeg import FFmpegProxy, FFmpegSection, FFprobeProxy
from cvp.popups.open_file import OpenFilePopup
from cvp.process.manager import ProcessManager
from cvp.resources.download.links.ffmpeg import FFMPEG_LINKS, FFPROBE_LINKS, LinkMap
from cvp.system.platform import SysMach, get_system_machine
from cvp.types import override
from cvp.widgets import button_ex, item_width
from cvp.widgets.hoc.popup import Popup, PopupPropagator
from cvp.widgets.hoc.tab import TabBar, TabItem


class ExeItem(TabItem, PopupPropagator):
    def __init__(
        self,
        filename: str,
        proxy: ValueProxy,
        links: LinkMap,
        pm: ProcessManager,
    ):
        super().__init__(filename)
        self._filename = filename
        self._proxy = proxy
        self._links = links
        self._pm = pm

        self._sms = list(str(sm) for sm in SysMach)
        self._current_sm = get_system_machine()
        self._current_sm_index = self._sms.index(str(self._current_sm))
        self._sms_index = self._current_sm_index

        self._browser = OpenFilePopup(
            f"Select {self._filename} executable",
            target=self.on_browser,
        )

    @property
    @override
    def popups(self) -> Sequence[Popup]:
        return [self._browser]

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
                "##Path",
                self.exe_path,
                imgui.INPUT_TEXT_ENTER_RETURNS_TRUE,
            )

        path_changed = path_result[0]
        if path_changed:
            path_value = path_result[1]
            assert isinstance(path_value, str)
            self.exe_path = path_value

        if imgui.button("Default"):
            self.exe_path = self._filename

        imgui.same_line()
        which_path = which(self._filename)
        if button_ex("Which", disabled=not which_path):
            assert isinstance(which_path, str)
            self.exe_path = which_path

        imgui.same_line()
        if button_ex("Cache"):
            pass

        imgui.same_line()
        if button_ex("Browse"):
            self._browser.show()

        imgui.separator()

        imgui.text("Download statically compiled executables")

        self._sms_index = imgui.combo("##SysMach", self._sms_index, self._sms)[1]
        sys_mach = SysMach(self._sms[self._sms_index])

        imgui.same_line()
        if imgui.button("Check current platform"):
            self._sms_index = self._current_sm_index

        link = self._links.get(sys_mach)
        if link is None:
            imgui.text_colored("This platform is not supported", 1.0, 0.1, 0.1)
            return

        if self._sms_index != self._current_sm_index:
            imgui.text_colored("Does not match the current platform", 1.0, 1.0, 0.0)


class ExeTabs(TabBar, PopupPropagator):
    def __init__(self, section: FFmpegSection, pm: ProcessManager):
        super().__init__()
        self.register(ExeItem("ffmpeg", FFmpegProxy(section), FFMPEG_LINKS, pm))
        self.register(ExeItem("ffprobe", FFprobeProxy(section), FFPROBE_LINKS, pm))

    @property
    @override
    def popups(self) -> Sequence[Popup]:
        result: List[Popup] = list()
        for item in self._items.values():
            if not isinstance(item, PopupPropagator):
                continue
            result.extend(item.popups)
        return result

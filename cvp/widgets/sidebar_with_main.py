# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from math import floor
from typing import Optional

import imgui

from cvp.config.sections.windows import BaseWindowSectionT, SidebarWidthProtocol
from cvp.context import Context
from cvp.gui import begin_child
from cvp.types import override
from cvp.variables import MIN_SIDEBAR_WIDTH, MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets.splitter_with_cursor import SplitterWithCursor
from cvp.widgets.window import Window


class SidebarWithMainInterface(ABC):
    @abstractmethod
    def on_process_sidebar(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_splitter(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_main(self) -> None:
        raise NotImplementedError


class SidebarWithMain(Window[BaseWindowSectionT], SidebarWithMainInterface):
    def __init__(
        self,
        context: Context,
        section: BaseWindowSectionT,
        title: Optional[str] = None,
        closable: Optional[bool] = None,
        flags: Optional[int] = None,
        min_width=MIN_WINDOW_WIDTH,
        min_height=MIN_WINDOW_HEIGHT,
        modifiable_title=False,
        min_sidebar_width=MIN_SIDEBAR_WIDTH,
    ):
        super().__init__(
            context=context,
            section=section,
            title=title,
            closable=closable,
            flags=flags,
            min_width=min_width,
            min_height=min_height,
            modifiable_title=modifiable_title,
        )

        self._min_sidebar_width = min_sidebar_width
        self._vertical_splitter = SplitterWithCursor.from_vertical("## VSplitter")

    @property
    def sidebar_width(self) -> int:
        section = self.section
        assert isinstance(section, SidebarWidthProtocol)
        return section.sidebar_width

    @sidebar_width.setter
    def sidebar_width(self, value: int) -> None:
        section = self.section
        assert isinstance(section, SidebarWidthProtocol)
        section.sidebar_width = value

    @override
    def on_process(self) -> None:
        with begin_child("## child_sidebar", self.sidebar_width, border=False):
            self.on_process_sidebar()

        imgui.same_line()
        self.on_process_splitter()
        imgui.same_line()

        with begin_child("## child_main", -1, -1):
            self.on_process_main()

    @override
    def on_process_sidebar(self) -> None:
        pass

    @override
    def on_process_splitter(self) -> None:
        split_result = self._vertical_splitter.do_process()
        if not split_result.changed:
            return

        sidebar_width_value = self.sidebar_width + floor(split_result.value)
        if sidebar_width_value < self._min_sidebar_width:
            sidebar_width_value = self._min_sidebar_width

        self.sidebar_width = sidebar_width_value

    @override
    def on_process_main(self) -> None:
        pass

# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional

import imgui

from cvp.config.sections import BaseSectionT
from cvp.config.sections.mixins.sidebar import SidebarWidthSectionMixin
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
    def on_process_main(self) -> None:
        raise NotImplementedError


class SidebarWithMain(Window[BaseSectionT], SidebarWithMainInterface):
    def __init__(
        self,
        context: Context,
        section: BaseSectionT,
        title: Optional[str] = None,
        closable: Optional[bool] = None,
        flags: Optional[int] = None,
        min_width=MIN_WINDOW_WIDTH,
        min_height=MIN_WINDOW_HEIGHT,
        modifiable_title=False,
        min_sidebar_width=MIN_SIDEBAR_WIDTH,
        sidebar_border=False,
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
        self._sidebar_border = sidebar_border
        self._sidebar_splitter = SplitterWithCursor.from_vertical("## VSplitter")

    @property
    def sidebar_section(self) -> SidebarWidthSectionMixin:
        assert isinstance(self.section, SidebarWidthSectionMixin)
        return self.section

    @property
    def sidebar_width(self) -> float:
        return self.sidebar_section.sidebar_width

    @sidebar_width.setter
    def sidebar_width(self, value: float) -> None:
        self.sidebar_section.sidebar_width = value

    def do_process_splitter(self) -> None:
        split_result = self._sidebar_splitter.do_process()
        if not split_result.changed:
            return

        value = self.sidebar_width + split_result.value
        if value < self._min_sidebar_width:
            value = self._min_sidebar_width

        self.sidebar_width = value

    @override
    def on_process(self) -> None:
        with begin_child(
            "## ChildSidebar",
            self.sidebar_width,
            border=self._sidebar_border,
        ):
            self.on_process_sidebar()

        imgui.same_line()
        self.do_process_splitter()
        imgui.same_line()

        with begin_child("## ChildMain"):
            self.on_process_main()

    @override
    def on_process_sidebar(self) -> None:
        pass

    @override
    def on_process_main(self) -> None:
        pass

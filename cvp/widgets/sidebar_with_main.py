# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional

import imgui

from cvp.config.sections import BaseSectionT
from cvp.config.sections.mixins.sidebar import Keys, SidebarWidthSectionMixin
from cvp.context import Context
from cvp.gui.begin_child import begin_child
from cvp.patterns.proxy import PropertyProxy
from cvp.types import override
from cvp.variables import (
    MAX_SIDEBAR_WIDTH,
    MIN_SIDEBAR_WIDTH,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
)
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
        max_sidebar_width=MAX_SIDEBAR_WIDTH,
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

        self._sidebar_border = sidebar_border
        self._sidebar_width = PropertyProxy[float](section, Keys.sidebar_width)
        self._sidebar_splitter = SplitterWithCursor.from_vertical(
            "## VSplitter",
            value_proxy=self._sidebar_width,
            min_value=min_sidebar_width,
            max_value=max_sidebar_width,
        )

    @property
    def sidebar_section(self) -> SidebarWidthSectionMixin:
        assert isinstance(self.section, SidebarWidthSectionMixin)
        return self.section

    @property
    def sidebar_width(self) -> float:
        value = self.sidebar_section.sidebar_width
        return self._sidebar_splitter.normalize_value(value)

    @sidebar_width.setter
    def sidebar_width(self, value: float) -> None:
        value = self._sidebar_splitter.normalize_value(value)
        self.sidebar_section.sidebar_width = value

    @override
    def on_process(self) -> None:
        with begin_child(
            "## ChildSidebar",
            self.sidebar_width,
            border=self._sidebar_border,
        ):
            self.on_process_sidebar()

        imgui.same_line()
        self._sidebar_splitter.do_process()
        imgui.same_line()

        with begin_child("## ChildMain"):
            self.on_process_main()

    @override
    def on_process_sidebar(self) -> None:
        pass

    @override
    def on_process_main(self) -> None:
        pass

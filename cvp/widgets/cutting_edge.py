# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from math import floor
from typing import Optional

import imgui

from cvp.config.sections.protocols.cutting_edge import SupportsCuttingEdge
from cvp.config.sections.windows import BaseWindowSectionT
from cvp.context import Context
from cvp.gui import begin_child
from cvp.types import override
from cvp.variables import (
    MIN_SIDEBAR_HEIGHT,
    MIN_SIDEBAR_WIDTH,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
)
from cvp.widgets.splitter_with_cursor import SplitterWithCursor
from cvp.widgets.window import Window


class CuttingEdgeInterface(ABC):
    @abstractmethod
    def on_process_sidebar_left(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_sidebar_right(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_main(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_bottom(self) -> None:
        raise NotImplementedError


class CuttingEdge(Window[BaseWindowSectionT], CuttingEdgeInterface):
    _cutting_edge_section: SupportsCuttingEdge
    _min_split_width: int
    _min_split_height: int
    _left_splitter: SplitterWithCursor
    _right_splitter: SplitterWithCursor
    _bottom_splitter: SplitterWithCursor

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
        min_sidebar_height=MIN_SIDEBAR_HEIGHT,
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

        if not isinstance(section, SupportsCuttingEdge):
            raise TypeError(
                "The 'section' argument must be compatible "
                f"with {SupportsCuttingEdge.__name__}"
            )

        self._cutting_edge_section = section
        self._min_split_width = min_sidebar_width
        self._min_split_height = min_sidebar_height

        self._left_splitter = SplitterWithCursor.from_vertical("## VSplitterLeft")
        self._right_splitter = SplitterWithCursor.from_vertical("## VSplitterRight")
        self._bottom_splitter = SplitterWithCursor.from_horizontal("## HSplitterBottom")

    @property
    def split_left(self) -> int:
        return self._cutting_edge_section.split_left

    @split_left.setter
    def split_left(self, value: int) -> None:
        self._cutting_edge_section.split_left = value

    @property
    def split_right(self) -> int:
        return self._cutting_edge_section.split_right

    @split_right.setter
    def split_right(self, value: int) -> None:
        self._cutting_edge_section.split_right = value

    @property
    def split_bottom(self) -> int:
        return self._cutting_edge_section.split_bottom

    @split_bottom.setter
    def split_bottom(self, value: int) -> None:
        self._cutting_edge_section.split_bottom = value

    @override
    def on_process(self) -> None:
        with begin_child("## ChildSidebarLeft", self.split_left):
            self.on_process_sidebar_left()

        imgui.same_line()
        self.do_split_left()
        imgui.same_line()

        with begin_child("## ChildCenter", -1 * self.split_right):
            with begin_child("## ChildMain", 0.0, -1 * self.split_bottom):
                self.on_process_main()
            self.do_split_bottom()
            with begin_child("## ChildBottom"):
                self.on_process_bottom()

        imgui.same_line()
        self.do_split_right()
        imgui.same_line()

        with begin_child("## ChildSidebarRight"):
            self.on_process_sidebar_right()

    def do_split_left(self) -> None:
        split_result = self._left_splitter.do_process()
        if not split_result.changed:
            return

        value = self.split_left + floor(split_result.value)
        if value < self._min_split_width:
            value = self._min_split_width

        self.split_left = value

    def do_split_right(self) -> None:
        split_result = self._right_splitter.do_process()
        if not split_result.changed:
            return

        value = self.split_right + floor(split_result.value)
        if value < self._min_split_width:
            value = self._min_split_width

        self.split_right = value

    def do_split_bottom(self) -> None:
        split_result = self._bottom_splitter.do_process()
        if not split_result.changed:
            return

        value = self.split_bottom + floor(split_result.value)
        if value < self._min_split_width:
            value = self._min_split_width

        self.split_bottom = value

    @override
    def on_process_sidebar_left(self) -> None:
        pass

    @override
    def on_process_sidebar_right(self) -> None:
        pass

    @override
    def on_process_main(self) -> None:
        pass

    @override
    def on_process_bottom(self) -> None:
        pass

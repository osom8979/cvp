# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional, Tuple

import imgui

from cvp.config.sections import BaseSectionT
from cvp.config.sections.mixins.cutting_edge import CuttingEdgeSectionMixin, Keys
from cvp.context import Context
from cvp.gui.begin_child import begin_child
from cvp.gui.cursor import cursor_pos_y
from cvp.gui.styles import style_item_spacing, style_window_padding
from cvp.logging.logging import widgets_logger as logger
from cvp.patterns.proxy import PropertyProxy
from cvp.types import override
from cvp.variables import (
    CUTTING_EDGE_PADDING_HEIGHT,
    CUTTING_EDGE_PADDING_WIDTH,
    MAX_SIDEBAR_HEIGHT,
    MAX_SIDEBAR_WIDTH,
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


class CuttingEdge(Window[BaseSectionT], CuttingEdgeInterface):
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
        min_sidebar_height=MIN_SIDEBAR_HEIGHT,
        max_sidebar_height=MAX_SIDEBAR_HEIGHT,
        padding_width=CUTTING_EDGE_PADDING_WIDTH,
        padding_height=CUTTING_EDGE_PADDING_HEIGHT,
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

        self._padding_width = padding_width
        self._padding_height = padding_height

        self._split_left = PropertyProxy[float](section, Keys.split_left)
        self._split_right = PropertyProxy[float](section, Keys.split_right)
        self._split_bottom = PropertyProxy[float](section, Keys.split_bottom)

        self._left_splitter = SplitterWithCursor.from_vertical(
            "## VSplitterLeft",
            value_proxy=self._split_left,
            min_value=min_sidebar_width,
            max_value=max_sidebar_width,
        )
        self._right_splitter = SplitterWithCursor.from_vertical(
            "## VSplitterRight",
            value_proxy=self._split_right,
            min_value=min_sidebar_width,
            max_value=max_sidebar_width,
            negative_delta=True,
        )
        self._bottom_splitter = SplitterWithCursor.from_horizontal(
            "## HSplitterBottom",
            value_proxy=self._split_bottom,
            min_value=min_sidebar_height,
            max_value=max_sidebar_height,
            negative_delta=True,
        )

    @property
    def cutting_edge_section(self) -> CuttingEdgeSectionMixin:
        assert isinstance(self.section, CuttingEdgeSectionMixin)
        return self.section

    @property
    def split_left(self) -> float:
        return self.cutting_edge_section.split_left

    @split_left.setter
    def split_left(self, value: float) -> None:
        self.cutting_edge_section.split_left = value

    @property
    def split_right(self) -> float:
        return self.cutting_edge_section.split_right

    @split_right.setter
    def split_right(self, value: float) -> None:
        self.cutting_edge_section.split_right = value

    @property
    def split_bottom(self) -> float:
        return self.cutting_edge_section.split_bottom

    @split_bottom.setter
    def split_bottom(self, value: float) -> None:
        self.cutting_edge_section.split_bottom = value

    @override
    def begin(self) -> Tuple[bool, bool]:
        with style_window_padding(0, 0):
            return super().begin()

    @override
    def on_process(self) -> None:
        pw = self._padding_width
        ph = self._padding_height
        top = imgui.get_cursor_pos_y()

        imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + pw)
        with begin_child("## ChildSidebarLeft", self.split_left):
            with style_item_spacing(0, 0):
                imgui.dummy(0, ph)
            self.on_process_sidebar_left()

        with style_item_spacing(pw, 0):
            imgui.same_line()

        with cursor_pos_y(top):
            self._left_splitter.do_process()
            if self._left_splitter.moving:
                logger.debug(repr(self._left_splitter))

        with style_item_spacing(-1, 0):
            imgui.same_line()

        with begin_child("## ChildCenter", -1 * self.split_right - pw):
            original_spacing = imgui.get_style().item_spacing
            with style_item_spacing(0, -1):
                with begin_child("## ChildMain", 0.0, -1 * self.split_bottom):
                    with style_item_spacing(*original_spacing):
                        self.on_process_main()

            with style_item_spacing(0, -1):
                self._bottom_splitter.do_process()
                if self._bottom_splitter.moving:
                    logger.debug(repr(self._bottom_splitter))

            imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + pw)
            with begin_child("## ChildBottom", -1 * pw):
                with style_item_spacing(0, 0):
                    imgui.dummy(0, ph)
                self.on_process_bottom()

        with style_item_spacing(-1, 0):
            imgui.same_line()

        with cursor_pos_y(top):
            self._right_splitter.do_process()
            if self._right_splitter.moving:
                logger.debug(repr(self._right_splitter))

        with style_item_spacing(pw, 0):
            imgui.same_line()

        with begin_child("## ChildSidebarRight", -1 * pw):
            with style_item_spacing(0, 0):
                imgui.dummy(0, ph)
            self.on_process_sidebar_right()

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
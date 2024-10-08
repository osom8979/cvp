# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional, Tuple, TypeVar

import imgui

from cvp.config.sections.bases.aui import AuiWindowConfig
from cvp.config.sections.proxies.aui import AuiBottomProxy, AuiLeftProxy, AuiRightProxy
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child
from cvp.imgui.cursor import cursor_pos_y
from cvp.imgui.styles import style_item_spacing, style_window_padding
from cvp.types import override
from cvp.variables import (
    AUI_PADDING_HEIGHT,
    AUI_PADDING_WIDTH,
    MAX_SIDEBAR_HEIGHT,
    MAX_SIDEBAR_WIDTH,
    MIN_SIDEBAR_HEIGHT,
    MIN_SIDEBAR_WIDTH,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
)
from cvp.widgets.splitter import Splitter
from cvp.widgets.window import Window

AuiSectionT = TypeVar("AuiSectionT", bound=AuiWindowConfig)


class AuiInterface(ABC):
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


class AuiWindow(Window[AuiSectionT], AuiInterface):
    def __init__(
        self,
        context: Context,
        window_config: AuiSectionT,
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
        padding_width=AUI_PADDING_WIDTH,
        padding_height=AUI_PADDING_HEIGHT,
    ):
        super().__init__(
            context=context,
            window_config=window_config,
            title=title,
            closable=closable,
            flags=flags,
            min_width=min_width,
            min_height=min_height,
            modifiable_title=modifiable_title,
        )

        self._padding_width = padding_width
        self._padding_height = padding_height

        self._split_left = AuiLeftProxy(window_config)
        self._split_right = AuiRightProxy(window_config)
        self._split_bottom = AuiBottomProxy(window_config)

        self._left_splitter = Splitter.from_vertical(
            "## VSplitterLeft",
            value_proxy=self._split_left,
            min_value=min_sidebar_width,
            max_value=max_sidebar_width,
        )
        self._right_splitter = Splitter.from_vertical(
            "## VSplitterRight",
            value_proxy=self._split_right,
            min_value=min_sidebar_width,
            max_value=max_sidebar_width,
            negative_delta=True,
        )
        self._bottom_splitter = Splitter.from_horizontal(
            "## HSplitterBottom",
            value_proxy=self._split_bottom,
            min_value=min_sidebar_height,
            max_value=max_sidebar_height,
            negative_delta=True,
        )

    @property
    def split_left(self) -> float:
        value = self.window_config.split_left
        return self._left_splitter.normalize_value(value)

    @split_left.setter
    def split_left(self, value: float) -> None:
        value = self._left_splitter.normalize_value(value)
        self.window_config.split_left = value

    @property
    def split_right(self) -> float:
        value = self.window_config.split_right
        return self._right_splitter.normalize_value(value)

    @split_right.setter
    def split_right(self, value: float) -> None:
        value = self._right_splitter.normalize_value(value)
        self.window_config.split_right = value

    @property
    def split_bottom(self) -> float:
        value = self.window_config.split_bottom
        return self._bottom_splitter.normalize_value(value)

    @split_bottom.setter
    def split_bottom(self, value: float) -> None:
        value = self._bottom_splitter.normalize_value(value)
        self.window_config.split_bottom = value

    @property
    def padding_width(self) -> float:
        return self._padding_width

    @property
    def padding_height(self) -> float:
        return self._padding_height

    @property
    def padding(self) -> Tuple[float, float]:
        return self._padding_width, self._padding_height

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

        with style_item_spacing(-1, 0):
            imgui.same_line()

        with begin_child("## ChildCenter", -self.split_right - pw):
            original_spacing = imgui.get_style().item_spacing
            with style_item_spacing(0, -1):
                with begin_child("## ChildMain", 0.0, -self.split_bottom):
                    with style_item_spacing(*original_spacing):
                        self.on_process_main()

            with style_item_spacing(0, -1):
                self._bottom_splitter.do_process()

            imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + pw)
            with begin_child("## ChildBottom", -pw):
                with style_item_spacing(0, 0):
                    imgui.dummy(0, ph)
                self.on_process_bottom()

        with style_item_spacing(-1, 0):
            imgui.same_line()

        with cursor_pos_y(top):
            self._right_splitter.do_process()

        with style_item_spacing(pw, 0):
            imgui.same_line()

        with begin_child("## ChildSidebarRight", -pw):
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

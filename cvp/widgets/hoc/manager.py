# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from math import floor
from typing import Generic, Mapping, Optional, TypeVar

import imgui

# noinspection PyProtectedMember
from cvp.config.sections.windows.manager._base import BaseManagerSection
from cvp.context import Context
from cvp.types import override
from cvp.variables import MIN_SIDEBAR_WIDTH, MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets import SplitterWithCursor, begin_child, text_centered
from cvp.widgets.hoc.window import Window

ManagerSectionT = TypeVar("ManagerSectionT", bound=BaseManagerSection)
MenuItemT = TypeVar("MenuItemT")


class ManagerInterface(Generic[MenuItemT], ABC):
    @abstractmethod
    def query_menu_title(self, key: str, item: MenuItemT) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_menus(self) -> Mapping[str, MenuItemT]:
        raise NotImplementedError

    @abstractmethod
    def on_process_sidebar(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_sidebar_top(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_sidebar_bottom(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_splitter(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_main(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_menu(self, key: str, item: MenuItemT) -> None:
        raise NotImplementedError


class Manager(Window[ManagerSectionT], ManagerInterface[MenuItemT]):
    _latest_menus: Optional[Mapping[str, MenuItemT]]

    def __init__(
        self,
        context: Context,
        section: ManagerSectionT,
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
        self._latest_menus = None
        self._splitter = SplitterWithCursor.from_vertical("## VSplitter")

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

    @property
    def latest_menus(self):
        return self._latest_menus

    @override
    def on_process(self) -> None:
        self._latest_menus = self.get_menus()
        self.on_process_sidebar()
        imgui.same_line()
        self.on_process_splitter()
        imgui.same_line()
        self.on_process_main()

    @override
    def query_menu_title(self, key: str, item: MenuItemT) -> str:
        if hasattr(item, "title"):
            return getattr(item, "title")
        elif hasattr(item, "label"):
            return getattr(item, "label")
        elif hasattr(item, "name"):
            return getattr(item, "name")
        else:
            return str(item)

    @override
    def get_menus(self) -> Mapping[str, MenuItemT]:
        return dict()

    @override
    def on_process_sidebar(self) -> None:
        assert self._latest_menus is not None

        with begin_child("## SideChild", self.sidebar_width, border=False):
            self.on_process_sidebar_top()
            self.on_process_sidebar_bottom()

    @override
    def on_process_sidebar_top(self) -> None:
        assert self._latest_menus is not None

    @override
    def on_process_sidebar_bottom(self) -> None:
        assert self._latest_menus is not None

        content_width = imgui.get_content_region_available_width()
        imgui.set_next_item_width(content_width)

        if imgui.begin_list_box("## SideList", width=-1, height=-1).opened:
            for key, menu in self._latest_menus.items():
                title = self.query_menu_title(key, menu)
                label = f"{title}##{key}"
                if imgui.selectable(label, key == self.selected)[1]:
                    self.selected = key
            imgui.end_list_box()

    @override
    def on_process_splitter(self) -> None:
        assert self._latest_menus is not None

        if splitter_result := self._splitter.do_process():
            sidebar_width_value = self.sidebar_width + floor(splitter_result.value)
            if sidebar_width_value < self._min_sidebar_width:
                sidebar_width_value = self._min_sidebar_width
            self.sidebar_width = sidebar_width_value

    @override
    def on_process_main(self) -> None:
        assert self._latest_menus is not None

        with begin_child("## MainChild", -1, -1):
            selected_menu = self._latest_menus.get(self.selected)
            if selected_menu is not None:
                self.on_menu(self.selected, selected_menu)
            else:
                text_centered("Please select a item")

    @override
    def on_menu(self, key: str, item: MenuItemT) -> None:
        pass

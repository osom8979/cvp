# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Generic, Mapping, Optional, TypeVar

import imgui

# noinspection PyProtectedMember
from cvp.config.sections.windows.manager._base import BaseManagerSection
from cvp.context import Context
from cvp.types import override
from cvp.variables import MIN_SIDEBAR_WIDTH
from cvp.widgets import begin_child, end_child, text_centered
from cvp.widgets.hoc.tab import ItemT, TabBar, TabItem
from cvp.widgets.hoc.window import Window

ManagerSectionT = TypeVar("ManagerSectionT", bound=BaseManagerSection)


class ItemsProxy(Generic[ItemT], ABC):
    @abstractmethod
    def __call__(self) -> Mapping[str, ItemT]:
        raise NotImplementedError


class ManagerWindow(Window[ManagerSectionT], Generic[ManagerSectionT, ItemT]):
    def __init__(
        self,
        context: Context,
        section: ManagerSectionT,
        proxy: ItemsProxy[ItemT],
        title: Optional[str] = None,
        closable: Optional[bool] = None,
        flags: Optional[int] = None,
        tabs_identifier: Optional[str] = None,
        tabs_flags=0,
        min_sidebar_width=MIN_SIDEBAR_WIDTH,
    ):
        super().__init__(
            context=context,
            section=section,
            title=title,
            closable=closable,
            flags=flags,
        )
        self._proxy = proxy
        self._tabs = TabBar[ItemT](
            context=context,
            identifier=tabs_identifier,
            flags=tabs_flags,
        )
        self._min_sidebar_width = min_sidebar_width

    def register(self, item: TabItem[ItemT]) -> None:
        self._tabs.register(item)

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

    def drag_sidebar_width(self) -> None:
        sidebar_width_result = imgui.drag_int(
            "## SideWidth",
            self.sidebar_width,
            1.0,
            self._min_sidebar_width,
            0,
            "Sidebar Width %d",
        )

        sidebar_width_changed = sidebar_width_result[0]
        assert isinstance(sidebar_width_changed, bool)

        if sidebar_width_changed:
            sidebar_width_value = sidebar_width_result[1]
            assert isinstance(sidebar_width_value, int)

            if sidebar_width_value < self._min_sidebar_width:
                sidebar_width_value = self._min_sidebar_width

            self.sidebar_width = sidebar_width_value

    @override
    def on_process(self) -> None:
        items = self._proxy()

        if begin_child("## SideChild", self.sidebar_width, border=True).visible:
            try:
                content_width = imgui.get_content_region_available_width()
                imgui.set_next_item_width(content_width)
                self.drag_sidebar_width()

                imgui.separator()

                if imgui.begin_list_box("## SideList", width=-1, height=-1).opened:
                    for key, item in items.items():

                        if hasattr(item, "title"):
                            title = getattr(item, "title")
                        elif hasattr(item, "label"):
                            title = getattr(item, "label")
                        elif hasattr(item, "name"):
                            title = getattr(item, "name")
                        else:
                            title = str(item)

                        label = f"{title}##{key}"
                        if imgui.selectable(label, key == self.selected)[1]:
                            self.selected = key
                    imgui.end_list_box()
            finally:
                end_child()

        imgui.same_line()

        if begin_child("## MainChild", -1, -1).visible:
            try:
                selected_item = items.get(self.selected)
                if selected_item is not None:
                    self._tabs.do_process(selected_item)
                else:
                    text_centered("Please select a item")
            finally:
                end_child()

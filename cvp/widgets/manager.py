# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from enum import StrEnum, unique
from typing import Generic, Mapping, Optional, TypeVar

import imgui

from cvp.config.sections import BaseSectionT
from cvp.config.sections.mixins.selected import SelectedSectionMixin
from cvp.context import Context
from cvp.gui.text_centered import text_centered
from cvp.types import override
from cvp.variables import MIN_SIDEBAR_WIDTH, MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets.sidebar_with_main import SidebarWithMain

MenuItemT = TypeVar("MenuItemT")


@unique
class MenuTitleKey(StrEnum):
    title_ = "title"
    label_ = "label"
    name_ = "name"


class ManagerInterface(Generic[MenuItemT], ABC):
    @abstractmethod
    def get_menus(self) -> Mapping[str, MenuItemT]:
        raise NotImplementedError

    @abstractmethod
    def query_menu_title(self, key: str, item: MenuItemT) -> str:
        raise NotImplementedError

    @abstractmethod
    def on_process_sidebar_top(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_sidebar_bottom(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_menu(self, key: str, item: MenuItemT) -> None:
        raise NotImplementedError


class Manager(SidebarWithMain[BaseSectionT], ManagerInterface[MenuItemT]):
    _latest_menus: Mapping[str, MenuItemT]

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
            min_sidebar_width=min_sidebar_width,
        )
        self._latest_menus = dict()

    @property
    def selected_section(self) -> SelectedSectionMixin:
        assert isinstance(self.section, SelectedSectionMixin)
        return self.section

    @property
    def selected(self) -> str:
        return self.selected_section.selected

    @selected.setter
    def selected(self, value: str) -> None:
        self.selected_section.selected = value

    @property
    def latest_menus(self):
        return self._latest_menus

    def update_menus(self) -> None:
        self._latest_menus = self.get_menus()

    @override
    def on_before(self) -> None:
        self.update_menus()

    @override
    def get_menus(self) -> Mapping[str, MenuItemT]:
        return dict()

    @override
    def query_menu_title(self, key: str, item: MenuItemT) -> str:
        if hasattr(item, MenuTitleKey.title_):
            return getattr(item, MenuTitleKey.title_)
        elif hasattr(item, MenuTitleKey.label_):
            return getattr(item, MenuTitleKey.label_)
        elif hasattr(item, MenuTitleKey.name_):
            return getattr(item, MenuTitleKey.name_)
        else:
            return str(item)

    @override
    def on_process_sidebar(self) -> None:
        self.on_process_sidebar_top()
        self.on_process_sidebar_bottom()

    @override
    def on_process_sidebar_top(self) -> None:
        pass

    @override
    def on_process_sidebar_bottom(self) -> None:
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
    def on_process_main(self) -> None:
        selected_menu = self._latest_menus.get(self.selected)
        if selected_menu is not None:
            self.on_menu(self.selected, selected_menu)
        else:
            text_centered("Please select a item")

    @override
    def on_menu(self, key: str, item: MenuItemT) -> None:
        pass
# -*- coding: utf-8 -*-

from abc import ABC
from typing import Optional

from cvp.context import Context
from cvp.types import override
from cvp.variables import MIN_SIDEBAR_WIDTH
from cvp.widgets.hoc.manager import Manager, ManagerSectionT, MenuItemT
from cvp.widgets.hoc.tab import TabBar, TabItem


class ManagerTab(Manager[ManagerSectionT, MenuItemT], ABC):
    def __init__(
        self,
        context: Context,
        section: ManagerSectionT,
        title: Optional[str] = None,
        closable: Optional[bool] = None,
        flags: Optional[int] = None,
        min_sidebar_width=MIN_SIDEBAR_WIDTH,
        tabs_identifier: Optional[str] = None,
        tabs_flags=0,
    ):
        super().__init__(
            context=context,
            section=section,
            title=title,
            closable=closable,
            flags=flags,
            min_sidebar_width=min_sidebar_width,
        )
        self._tabs = TabBar[MenuItemT](
            context=context,
            identifier=tabs_identifier,
            flags=tabs_flags,
        )

    def register(self, item: TabItem[MenuItemT]) -> None:
        self._tabs.register(item)

    @override
    def on_menu(self, key: str, item: MenuItemT) -> None:
        self._tabs.do_process(item)

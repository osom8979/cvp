# -*- coding: utf-8 -*-

from typing import Mapping, Optional

from cvp.context import Context
from cvp.types import override
from cvp.variables import MIN_SIDEBAR_WIDTH, MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets.manager import Manager, ManagerSectionT


class SidebarWithMain(Manager[ManagerSectionT, None]):
    __menus_faker__: Mapping[str, None] = dict()

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
            min_sidebar_width=min_sidebar_width,
        )

    @override
    def query_menu_title(self, key: str, item: None) -> str:
        raise NotImplementedError

    @override
    def get_menus(self) -> Mapping[str, None]:
        return self.__menus_faker__

    @override
    def on_menu(self, key: str, item: None) -> None:
        raise NotImplementedError

    @override
    def on_process_sidebar(self) -> None:
        pass

    @override
    def on_process_main(self) -> None:
        pass

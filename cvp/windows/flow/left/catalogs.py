# -*- coding: utf-8 -*-

from cvp.context import Context
from cvp.types import override
from cvp.widgets.tab import TabItem


class CatalogsTab(TabItem):
    def __init__(self, context: Context):
        super().__init__(context, "Catalogs")

    @override
    def on_item(self, item) -> None:
        pass

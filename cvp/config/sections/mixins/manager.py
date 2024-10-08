# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.config.sections.mixins.selected import SelectedMixin
from cvp.config.sections.mixins.sidebar import SidebarMixin
from cvp.config.sections.mixins.window import WindowMixin


@dataclass
class ManagerMixin(
    SelectedMixin,
    SidebarMixin,
    WindowMixin,
):
    pass

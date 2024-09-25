# -*- coding: utf-8 -*-

from cvp.config.sections.mixins.selected import SelectedSectionMixin
from cvp.config.sections.mixins.sidebar import SidebarWidthSectionMixin
from cvp.config.sections.mixins.window import WindowSectionMixin


class ManagerSectionMixin(
    SelectedSectionMixin,
    SidebarWidthSectionMixin,
    WindowSectionMixin,
):
    pass

# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.config.sections.bases.window import WindowConfig


@dataclass
class SidebarWindowConfig(WindowConfig):
    sidebar_width: float = 0.0

# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.config.sections.mixins.aui import AuiMixin
from cvp.config.sections.mixins.window import WindowMixin
from cvp.variables import MIN_SIDEBAR_HEIGHT


@dataclass
class FlowConfig(AuiMixin, WindowMixin):
    split_tree: float = float(MIN_SIDEBAR_HEIGHT)

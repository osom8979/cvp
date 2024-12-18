# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.config.sections.bases.aui import AuiWindowConfig
from cvp.variables import MIN_SIDEBAR_HEIGHT


@dataclass
class FlowAuiConfig(AuiWindowConfig):
    split_tree: float = MIN_SIDEBAR_HEIGHT
    min_split_tree: float = MIN_SIDEBAR_HEIGHT

# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

from cvp.config.sections.bases.manager import ManagerWindowConfig


@dataclass
class WindowManagerConfig(ManagerWindowConfig):
    begin_order: List[str] = field(default_factory=list)

# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

from cvp.config.sections.bases.manager import ManagerWindowConfig


@dataclass
class WindowManagerConfig(ManagerWindowConfig):
    begin_order: List[str] = field(default_factory=list)

    def appendleft_begin_order(self, key: str) -> None:
        try:
            index = self.begin_order.index(key)
        except ValueError:
            self.begin_order = [key] + self.begin_order
        else:
            self.begin_order = [self.begin_order.pop(index)] + self.begin_order

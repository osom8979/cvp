# -*- coding: utf-8 -*-

from typing import Optional


class FlowGraph:
    def __init__(self, name: Optional[str] = None):
        self._name = name if name else str()

    @property
    def name(self):
        return self._name

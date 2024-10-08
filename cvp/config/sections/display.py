# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Tuple


@dataclass
class DisplayConfig:
    width: int = -1
    height: int = -1
    fullscreen: bool = False

    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height

    @size.setter
    def size(self, value: Tuple[int, int]) -> None:
        self.width = value[0]
        self.height = value[1]

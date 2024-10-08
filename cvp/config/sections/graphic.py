# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional


@dataclass
class GraphicConfig:
    force_egl: Optional[bool] = None
    use_accelerate: Optional[bool] = None

    @property
    def force_egl_environ(self) -> str:
        return "1" if self.force_egl else "0"

    @property
    def use_accelerate_environ(self) -> str:
        return "1" if self.use_accelerate else "0"

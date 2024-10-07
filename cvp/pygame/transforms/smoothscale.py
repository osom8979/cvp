# -*- coding: utf-8 -*-

from typing import Sequence

from cvp.pygame.transforms._base import TransformBase
from cvp.pygame.types import SequenceProtocol
from cvp.types import override
from pygame.surface import Surface
from pygame.transform import smoothscale


class SmoothscaleTransform(TransformBase):
    def __init__(self, size: Sequence[float]):
        self.size = size

    @override
    def transform(self, source: Surface) -> Surface:
        assert isinstance(self.size, SequenceProtocol)
        return smoothscale(source, self.size)

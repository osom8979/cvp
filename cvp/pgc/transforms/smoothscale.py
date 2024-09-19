# -*- coding: utf-8 -*-

from typing import Sequence

from overrides import override
from pygame.surface import Surface
from pygame.transform import smoothscale

from cvp.pgc.transforms._base import TransformBase
from cvp.pgc.types import SequenceProtocol


class SmoothscaleTransform(TransformBase):
    def __init__(self, size: Sequence[float]):
        self.size = size

    @override
    def transform(self, source: Surface) -> Surface:
        assert isinstance(self.size, SequenceProtocol)
        return smoothscale(source, self.size)

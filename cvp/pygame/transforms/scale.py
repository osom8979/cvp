# -*- coding: utf-8 -*-

from typing import Sequence

from pygame.surface import Surface
from pygame.transform import scale

from cvp.pygame.transforms._base import TransformBase
from cvp.pygame.types import SequenceProtocol
from cvp.types.override import override


class ScaleTransform(TransformBase):
    def __init__(self, size: Sequence[float]):
        self.size = size

    @override
    def transform(self, source: Surface) -> Surface:
        assert isinstance(self.size, SequenceProtocol)
        return scale(source, self.size)

# -*- coding: utf-8 -*-

from overrides import override
from pygame.surface import Surface
from pygame.transform import scale

from cvp.renderer.pygame.transforms._base import TransformBase
from cvp.renderer.pygame.types import Sequence


class ScaleTransform(TransformBase):
    def __init__(self, size: Sequence[float]):
        self.size = size

    @override
    def transform(self, source: Surface) -> Surface:
        return scale(source, self.size)

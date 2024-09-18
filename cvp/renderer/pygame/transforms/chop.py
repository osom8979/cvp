# -*- coding: utf-8 -*-

from overrides import override
from pygame.surface import Surface
from pygame.transform import chop

from cvp.renderer.pygame.transforms._base import TransformBase
from cvp.renderer.pygame.types import RectValue


class ChopTransform(TransformBase):
    def __init__(self, rect: RectValue):
        self.rect = rect

    @override
    def transform(self, source: Surface) -> Surface:
        return chop(source, self.rect)

# -*- coding: utf-8 -*-

from pygame.surface import Surface
from pygame.transform import chop

from cvp.pygame.transforms._base import TransformBase
from cvp.pygame.types import RectValue
from cvp.types.override import override


class ChopTransform(TransformBase):
    def __init__(self, rect: RectValue):
        self.rect = rect

    @override
    def transform(self, source: Surface) -> Surface:
        return chop(source, self.rect)

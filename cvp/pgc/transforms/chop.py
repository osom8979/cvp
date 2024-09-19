# -*- coding: utf-8 -*-

from pygame.surface import Surface
from pygame.transform import chop

from cvp.pgc.transforms._base import TransformBase
from cvp.pgc.types import RectValue
from cvp.types import override


class ChopTransform(TransformBase):
    def __init__(self, rect: RectValue):
        self.rect = rect

    @override
    def transform(self, source: Surface) -> Surface:
        return chop(source, self.rect)

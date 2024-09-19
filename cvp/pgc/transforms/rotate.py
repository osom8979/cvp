# -*- coding: utf-8 -*-

from pygame.surface import Surface
from pygame.transform import rotate

from cvp.pgc.transforms._base import TransformBase
from cvp.types import override


class RotateTransform(TransformBase):
    def __init__(self, angle: float):
        self.angle = angle

    @override
    def transform(self, source: Surface) -> Surface:
        return rotate(source, self.angle)

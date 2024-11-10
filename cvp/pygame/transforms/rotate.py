# -*- coding: utf-8 -*-

from pygame.surface import Surface
from pygame.transform import rotate

from cvp.pygame.transforms._base import TransformBase
from cvp.types.override import override


class RotateTransform(TransformBase):
    def __init__(self, angle: float):
        self.angle = angle

    @override
    def transform(self, source: Surface) -> Surface:
        return rotate(source, self.angle)

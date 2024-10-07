# -*- coding: utf-8 -*-

from cvp.pygame.transforms._base import TransformBase
from cvp.types import override
from pygame.surface import Surface
from pygame.transform import rotozoom


class RotozoomTransform(TransformBase):
    def __init__(self, angle: float, scale: float):
        self.angle = angle
        self.scale = scale

    @override
    def transform(self, source: Surface) -> Surface:
        return rotozoom(source, self.angle, self.scale)

# -*- coding: utf-8 -*-

from overrides import override
from pygame.surface import Surface
from pygame.transform import rotate

from cvp.renderer.pygame.transforms._base import TransformBase


class RotateTransform(TransformBase):
    def __init__(self, angle: float):
        self.angle = angle

    @override
    def transform(self, source: Surface) -> Surface:
        return rotate(source, self.angle)

# -*- coding: utf-8 -*-

from overrides import override
from pygame.surface import Surface
from pygame.transform import grayscale

from cvp.renderer.pygame.transforms._base import TransformBase


class GrayscaleTransform(TransformBase):
    @override
    def transform(self, source: Surface) -> Surface:
        return grayscale(source)

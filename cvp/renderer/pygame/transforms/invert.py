# -*- coding: utf-8 -*-

from overrides import override
from pygame.surface import Surface
from pygame.transform import invert

from cvp.renderer.pygame.transforms._base import TransformBase


class InvertTransform(TransformBase):
    @override
    def transform(self, source: Surface) -> Surface:
        return invert(source)

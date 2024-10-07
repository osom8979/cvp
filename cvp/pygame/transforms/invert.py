# -*- coding: utf-8 -*-

from cvp.pygame.transforms._base import TransformBase
from cvp.types import override
from pygame.surface import Surface
from pygame.transform import invert


class InvertTransform(TransformBase):
    @override
    def transform(self, source: Surface) -> Surface:
        return invert(source)

# -*- coding: utf-8 -*-

from overrides import override
from pygame.surface import Surface
from pygame.transform import flip

from cvp.pgc.transforms._base import TransformBase


class FlipTransform(TransformBase):
    def __init__(self, flip_x=False, flip_y=False):
        self.flip_x = flip_x
        self.flip_y = flip_y

    @override
    def transform(self, source: Surface) -> Surface:
        return flip(source, self.flip_x, self.flip_y)

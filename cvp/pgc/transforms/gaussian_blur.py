# -*- coding: utf-8 -*-

from overrides import override
from pygame.surface import Surface
from pygame.transform import gaussian_blur

from cvp.pgc.transforms._base import TransformBase


class GaussianBlurTransform(TransformBase):
    def __init__(
        self,
        radius: int,
        repeat_edge_pixels=True,
    ):
        self.radius = radius
        self.repeat_edge_pixels = repeat_edge_pixels

    @override
    def transform(self, source: Surface) -> Surface:
        return gaussian_blur(source, self.radius, self.repeat_edge_pixels)

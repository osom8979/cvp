# -*- coding: utf-8 -*-

from cvp.pygame.transforms._base import TransformBase
from cvp.types import override
from pygame.surface import Surface
from pygame.transform import box_blur


class BoxBlurTransform(TransformBase):
    def __init__(
        self,
        radius: int,
        repeat_edge_pixels=True,
    ):
        self.radius = radius
        self.repeat_edge_pixels = repeat_edge_pixels

    @override
    def transform(self, source: Surface) -> Surface:
        return box_blur(source, self.radius, self.repeat_edge_pixels)

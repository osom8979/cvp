# -*- coding: utf-8 -*-

from overrides import override
from pygame.surface import Surface
from pygame.transform import laplacian

from cvp.renderer.pygame.transforms._base import TransformBase


class LaplacianTransform(TransformBase):
    @override
    def transform(self, source: Surface) -> Surface:
        return laplacian(source)

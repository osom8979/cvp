# -*- coding: utf-8 -*-

from pygame.surface import Surface
from pygame.transform import laplacian

from cvp.pgc.transforms._base import TransformBase
from cvp.types import override


class LaplacianTransform(TransformBase):
    @override
    def transform(self, source: Surface) -> Surface:
        return laplacian(source)
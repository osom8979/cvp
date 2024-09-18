# -*- coding: utf-8 -*-

from overrides import override
from pygame.surface import Surface
from pygame.transform import scale2x

from cvp.pgc.transforms._base import TransformBase


class Scale2xTransform(TransformBase):
    @override
    def transform(self, source: Surface) -> Surface:
        return scale2x(source)

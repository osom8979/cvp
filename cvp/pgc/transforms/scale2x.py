# -*- coding: utf-8 -*-

from pygame.surface import Surface
from pygame.transform import scale2x

from cvp.pgc.transforms._base import TransformBase
from cvp.types import override


class Scale2xTransform(TransformBase):
    @override
    def transform(self, source: Surface) -> Surface:
        return scale2x(source)
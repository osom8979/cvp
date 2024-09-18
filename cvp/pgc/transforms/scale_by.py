# -*- coding: utf-8 -*-

from typing import Union

from overrides import override
from pygame.surface import Surface
from pygame.transform import scale_by

from cvp.pgc.transforms._base import TransformBase
from cvp.pgc.types import Sequence


class ScaleByTransform(TransformBase):
    def __init__(self, factor: Union[float, Sequence[float]]):
        self.factor = factor

    @override
    def transform(self, source: Surface) -> Surface:
        return scale_by(source, self.factor)

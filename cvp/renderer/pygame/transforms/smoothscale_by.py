# -*- coding: utf-8 -*-

from typing import Union

from overrides import override
from pygame.surface import Surface
from pygame.transform import smoothscale_by

from cvp.renderer.pygame.transforms._base import TransformBase
from cvp.renderer.pygame.types import Sequence


class SmoothscaleByTransform(TransformBase):
    def __init__(self, factor: Union[float, Sequence[float]]):
        self.factor = factor

    @override
    def transform(self, source: Surface) -> Surface:
        return smoothscale_by(source, self.factor)

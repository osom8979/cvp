# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections.protocols.cutting_edge import SupportsCuttingEdge
from cvp.config.sections.windows._base import BaseWindowSection
from cvp.types import override
from cvp.variables import MIN_SIDEBAR_HEIGHT, MIN_SIDEBAR_WIDTH


@unique
class _Keys(StrEnum):
    split_left = auto()
    split_right = auto()
    split_bottom = auto()


class FlowSection(BaseWindowSection, SupportsCuttingEdge[float]):
    K = _Keys

    def __init__(self, config: BaseConfig, section="flow"):
        super().__init__(config=config, section=section)

    # noinspection PyProtocol
    @property
    @override
    def split_left(self) -> float:
        return self.get(self.K.split_left, MIN_SIDEBAR_WIDTH)

    @split_left.setter
    @override
    def split_left(self, value: float) -> None:
        self.set(self.K.split_left, value)

    # noinspection PyProtocol
    @property
    @override
    def split_right(self) -> float:
        return self.get(self.K.split_right, MIN_SIDEBAR_WIDTH)

    @split_right.setter
    @override
    def split_right(self, value: float) -> None:
        self.set(self.K.split_right, value)

    # noinspection PyProtocol
    @property
    @override
    def split_bottom(self) -> float:
        return self.get(self.K.split_bottom, MIN_SIDEBAR_HEIGHT)

    @split_bottom.setter
    @override
    def split_bottom(self, value: float) -> None:
        self.set(self.K.split_bottom, value)

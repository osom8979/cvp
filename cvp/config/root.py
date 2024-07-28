# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from os import PathLike
from typing import Optional, Union

from cvp.config._base import BaseConfig
from cvp.config.sections.display import DisplaySection
from cvp.config.sections.font import FontSection
from cvp.config.sections.overlay import OverlaySection


@unique
class Section(StrEnum):
    DEFAULT = auto()
    font = auto()
    overlay = auto()
    views = auto()
    tools = auto()


@unique
class Key(StrEnum):
    # [DEFAULT]
    open_file_popup_path = auto()

    # [views]
    overlay = auto()

    # [tools]
    demo = auto()


class Config(BaseConfig):
    S = Section
    K = Key

    def __init__(self, filename: Optional[Union[str, PathLike]] = None):
        super().__init__(filename)
        self._display = DisplaySection(self)
        self._font = FontSection(self)
        self._overlay = OverlaySection(self)

    @property
    def display(self):
        return self._display

    @property
    def font(self):
        return self._font

    @property
    def overlay(self):
        return self._overlay

    @property
    def views_overlay(self) -> bool:
        return self.get(self.S.views, self.K.overlay, False)

    @views_overlay.setter
    def views_overlay(self, value: bool) -> None:
        self.set(self.S.views, self.K.overlay, value)

    @property
    def tools_demo(self) -> bool:
        return self.get(self.S.tools, self.K.demo, False)

    @tools_demo.setter
    def tools_demo(self, value: bool) -> None:
        self.set(self.S.tools, self.K.demo, value)

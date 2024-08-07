# -*- coding: utf-8 -*-

from os import PathLike
from typing import List, Optional, Union

from cvp.config._base import BaseConfig
from cvp.config.sections.av import AvSection, filter_av_sections
from cvp.config.sections.default import DefaultSection
from cvp.config.sections.display import DisplaySection
from cvp.config.sections.font import FontSection
from cvp.config.sections.overlay import OverlaySection
from cvp.config.sections.tools import ToolsSection


class Config(BaseConfig):
    def __init__(self, filename: Optional[Union[str, PathLike]] = None):
        super().__init__(filename)
        self._default = DefaultSection(self)
        self._display = DisplaySection(self)
        self._font = FontSection(self)
        self._overlay = OverlaySection(self)
        self._tools = ToolsSection(self)

    @property
    def default(self):
        return self._default

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
    def tools(self):
        return self._tools

    def av_sections(self) -> List[str]:
        return filter_av_sections(self.sections())

    @property
    def avs(self) -> List[AvSection]:
        return [AvSection(section, self) for section in self.av_sections()]

    def create_av(self, name: str) -> AvSection:
        return AvSection.from_name(name, self)

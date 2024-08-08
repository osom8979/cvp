# -*- coding: utf-8 -*-

from os import PathLike
from typing import List, Optional, Union
from uuid import uuid4

from cvp.config._base import BaseConfig
from cvp.config.prefix import SectionPrefix
from cvp.config.sections.av import AvSection
from cvp.config.sections.demo import DemoSection
from cvp.config.sections.display import DisplaySection
from cvp.config.sections.font import FontSection
from cvp.config.sections.mpv import MpvSection
from cvp.config.sections.overlay import OverlaySection


class Config(BaseConfig):
    def __init__(
        self,
        filename: Optional[Union[str, PathLike]] = None,
        cvp_home: Optional[str] = None,
    ):
        super().__init__(filename=filename, cvp_home=cvp_home)
        self._avs = SectionPrefix(config=self, prefix="av.")
        self._demo = DemoSection(config=self)
        self._display = DisplaySection(config=self)
        self._font = FontSection(config=self)
        self._mpv = MpvSection(config=self)
        self._overlay = OverlaySection(config=self)

    def add_av_section(self, name: Optional[str] = None):
        section = self._avs.join_section_name(name if name else str(uuid4()))
        if self.has_section(section):
            raise KeyError(f"Section '{section}' already exists")
        return AvSection(config=self, section=section)

    @property
    def avs(self) -> List[AvSection]:
        sections = self._avs.sections()
        return [AvSection(config=self, section=section) for section in sections]

    @property
    def demo(self):
        return self._demo

    @property
    def display(self):
        return self._display

    @property
    def font(self):
        return self._font

    @property
    def mpv(self):
        return self._mpv

    @property
    def overlay(self):
        return self._overlay

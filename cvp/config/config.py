# -*- coding: utf-8 -*-

from os import PathLike
from typing import Dict, Optional, Union
from uuid import uuid4

from cvp.config._base import BaseConfig
from cvp.config.prefix import SectionPrefix
from cvp.config.sections.demo import DemoSection
from cvp.config.sections.display import DisplaySection
from cvp.config.sections.font import FontSection
from cvp.config.sections.manager import ManagerSection
from cvp.config.sections.media import MediaSection
from cvp.config.sections.mpv import MpvSection
from cvp.config.sections.overlay import OverlaySection
from cvp.config.sections.preference import PreferenceSection
from cvp.variables import MEDIA_SECTION_PREFIX


class Config(BaseConfig):
    def __init__(
        self,
        filename: Optional[Union[str, PathLike]] = None,
        cvp_home: Optional[str] = None,
    ):
        super().__init__(filename=filename, cvp_home=cvp_home)
        self._medias = SectionPrefix(config=self, prefix=MEDIA_SECTION_PREFIX)
        self._demo = DemoSection(config=self)
        self._display = DisplaySection(config=self)
        self._font = FontSection(config=self)
        self._manager = ManagerSection(self)
        self._mpv = MpvSection(config=self)
        self._overlay = OverlaySection(config=self)
        self._preference = PreferenceSection(config=self)

    def add_media_section(self, name: Optional[str] = None):
        section = self._medias.join_section_name(name if name else str(uuid4()))
        if self.has_section(section):
            raise KeyError(f"Section '{section}' already exists")
        return MediaSection(config=self, section=section)

    @property
    def medias(self) -> Dict[str, MediaSection]:
        result = dict()
        for section in self._medias.sections():
            key = self._medias.split_section_name(section)
            result[key] = MediaSection(config=self, section=section)
        return result

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
    def manager(self):
        return self._manager

    @property
    def mpv(self):
        return self._mpv

    @property
    def overlay(self):
        return self._overlay

    @property
    def preference(self):
        return self._preference

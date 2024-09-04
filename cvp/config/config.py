# -*- coding: utf-8 -*-

from collections import OrderedDict
from os import PathLike
from typing import Optional, Union
from uuid import uuid4

from cvp.config._base import BaseConfig
from cvp.config.prefix import SectionPrefix
from cvp.config.sections.appearance import AppearanceSection
from cvp.config.sections.concurrency import ConcurrencySection
from cvp.config.sections.developer import DeveloperSection
from cvp.config.sections.display import DisplaySection
from cvp.config.sections.ffmpeg import FFmpegSection
from cvp.config.sections.font import FontSection
from cvp.config.sections.logging import LoggingSection
from cvp.config.sections.windows.demo import DemoSection
from cvp.config.sections.windows.media import MediaSection
from cvp.config.sections.windows.medias import MediasSection
from cvp.config.sections.windows.mpv import MpvSection
from cvp.config.sections.windows.overlay import OverlaySection
from cvp.config.sections.windows.preference import PreferenceSection
from cvp.config.sections.windows.processes import ProcessesSection
from cvp.variables import MEDIA_SECTION_PREFIX


class Config(BaseConfig):
    def __init__(
        self,
        filename: Optional[Union[str, PathLike[str]]] = None,
        cvp_home: Optional[Union[str, PathLike[str]]] = None,
    ):
        super().__init__(filename=filename, cvp_home=cvp_home)
        self._medias = SectionPrefix(self, prefix=MEDIA_SECTION_PREFIX)
        self._appearance = AppearanceSection(self)
        self._concurrency = ConcurrencySection(self)
        self._demo = DemoSection(self)
        self._developer = DeveloperSection(self)
        self._display = DisplaySection(self)
        self._ffmpeg = FFmpegSection(self)
        self._font = FontSection(self)
        self._logging = LoggingSection(self)
        self._manager = MediasSection(self)
        self._mpv = MpvSection(self)
        self._overlay = OverlaySection(self)
        self._preference = PreferenceSection(self)
        self._processes = ProcessesSection(self)

    def add_media_section(self, name: Optional[str] = None):
        section = self._medias.join_section_name(name if name else str(uuid4()))
        if self.has_section(section):
            raise KeyError(f"Section '{section}' already exists")
        return MediaSection(config=self, section=section)

    @property
    def debug(self):
        return self._developer.debug

    @property
    def verbose(self):
        return self._developer.verbose

    @property
    def medias(self):
        result = OrderedDict[str, MediaSection]()
        for section in self._medias.sections():
            key = self._medias.split_section_name(section)
            result[key] = MediaSection(config=self, section=section)
        return result

    @property
    def appearance(self):
        return self._appearance

    @property
    def concurrency(self):
        return self._concurrency

    @property
    def demo(self):
        return self._demo

    @property
    def developer(self):
        return self._developer

    @property
    def display(self):
        return self._display

    @property
    def ffmpeg(self):
        return self._ffmpeg

    @property
    def font(self):
        return self._font

    @property
    def logging(self):
        return self._logging

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

    @property
    def processes(self):
        return self._processes

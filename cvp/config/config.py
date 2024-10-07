# -*- coding: utf-8 -*-

from collections import OrderedDict
from os import PathLike
from typing import Optional, Union
from uuid import uuid4

from cvp.config._base import BaseConfig
from cvp.config.prefix import SectionPrefix
from cvp.config.sections.appearance import AppearanceSection
from cvp.config.sections.concurrency import ConcurrencySection
from cvp.config.sections.context import ContextSection
from cvp.config.sections.developer import DeveloperSection
from cvp.config.sections.display import DisplaySection
from cvp.config.sections.ffmpeg import FFmpegSection
from cvp.config.sections.flow_window import FlowWindowSection
from cvp.config.sections.font import FontSection
from cvp.config.sections.graphic import GraphicSection
from cvp.config.sections.labeling import LabelingSection
from cvp.config.sections.layout import LayoutSection
from cvp.config.sections.layouts import LayoutsSection
from cvp.config.sections.logging import LoggingSection
from cvp.config.sections.media_window import MediaWindowSection
from cvp.config.sections.medias import MediasSection
from cvp.config.sections.overlay_window import OverlayWindowSection
from cvp.config.sections.preference import PreferenceSection
from cvp.config.sections.process import ProcessSection
from cvp.config.sections.stitching import StitchingSection
from cvp.config.sections.window import WindowSection
from cvp.variables import LAYOUT_SECTION_PREFIX, MEDIA_SECTION_PREFIX


class Config(BaseConfig):
    def __init__(
        self,
        filename: Optional[Union[str, PathLike[str]]] = None,
        cvp_home: Optional[Union[str, PathLike[str]]] = None,
    ):
        super().__init__(filename=filename, cvp_home=cvp_home)

        # Prefixes
        self._layout_prefix = SectionPrefix(self, prefix=LAYOUT_SECTION_PREFIX)
        self._media_prefix = SectionPrefix(self, prefix=MEDIA_SECTION_PREFIX)

        # Managers
        self.preference_manager = PreferenceSection(self)
        self.process_manager = ProcessSection(self)
        self.stitching_manager = StitchingSection(self)
        self.window_manager = WindowSection(self)
        self.labeling_manager = LabelingSection(self)
        self.layout_manager = LayoutsSection(self)
        self.media_manager = MediasSection(self)

        # Windows
        self.flow_window = FlowWindowSection(self)
        self.overlay_window = OverlayWindowSection(self)

        # Common
        self.appearance = AppearanceSection(self)
        self.concurrency = ConcurrencySection(self)
        self.context = ContextSection(self)
        self.developer = DeveloperSection(self)
        self.display = DisplaySection(self)
        self.ffmpeg = FFmpegSection(self)
        self.font = FontSection(self)
        self.graphic = GraphicSection(self)
        self.logging = LoggingSection(self)

    def add_layout_section(self, name: Optional[str] = None):
        section = self._layout_prefix.join_section_name(name if name else str(uuid4()))
        if self.has_section(section):
            raise KeyError(f"Section '{section}' already exists")
        return LayoutSection(config=self, section=section)

    def add_media_section(self, name: Optional[str] = None):
        section = self._media_prefix.join_section_name(name if name else str(uuid4()))
        if self.has_section(section):
            raise KeyError(f"Section '{section}' already exists")
        return MediaWindowSection(config=self, section=section)

    @property
    def layout_sections(self):
        result = OrderedDict[str, LayoutSection]()
        for section in self._layout_prefix.sections():
            key = self._layout_prefix.split_section_name(section)
            result[key] = LayoutSection(config=self, section=section)
        return result

    @property
    def media_sections(self):
        result = OrderedDict[str, MediaWindowSection]()
        for section in self._media_prefix.sections():
            key = self._media_prefix.split_section_name(section)
            result[key] = MediaWindowSection(config=self, section=section)
        return result

    @property
    def debug(self):
        return self.developer.debug

    @property
    def verbose(self):
        return self.developer.verbose

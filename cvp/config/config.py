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
from cvp.config.sections.font import FontSection
from cvp.config.sections.graphic import GraphicSection
from cvp.config.sections.logging import LoggingSection
from cvp.config.sections.windows.flow import FlowSection
from cvp.config.sections.windows.layout import LayoutSection
from cvp.config.sections.windows.manager.labeling import LabelingManagerSection
from cvp.config.sections.windows.manager.layout import LayoutManagerSection
from cvp.config.sections.windows.manager.media import MediaManagerSection
from cvp.config.sections.windows.manager.preference import PreferenceManagerSection
from cvp.config.sections.windows.manager.process import ProcessManagerSection
from cvp.config.sections.windows.manager.stitching import StitchingManagerSection
from cvp.config.sections.windows.manager.window import WindowManagerSection
from cvp.config.sections.windows.media import MediaSection
from cvp.config.sections.windows.overlay import OverlaySection
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
        self.preference_manager = PreferenceManagerSection(self)
        self.process_manager = ProcessManagerSection(self)
        self.stitching_manager = StitchingManagerSection(self)
        self.window_manager = WindowManagerSection(self)
        self.labeling_manager = LabelingManagerSection(self)
        self.layout_manager = LayoutManagerSection(self)
        self.media_manager = MediaManagerSection(self)

        # Windows
        self.flow = FlowSection(self)
        self.overlay = OverlaySection(self)

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
        return MediaSection(config=self, section=section)

    @property
    def layout_sections(self):
        result = OrderedDict[str, LayoutSection]()
        for section in self._layout_prefix.sections():
            key = self._layout_prefix.split_section_name(section)
            result[key] = LayoutSection(config=self, section=section)
        return result

    @property
    def media_sections(self):
        result = OrderedDict[str, MediaSection]()
        for section in self._media_prefix.sections():
            key = self._media_prefix.split_section_name(section)
            result[key] = MediaSection(config=self, section=section)
        return result

    @property
    def debug(self):
        return self.developer.debug

    @property
    def verbose(self):
        return self.developer.verbose

# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass, field
from os import PathLike
from typing import List, Union

from type_serialize import deserialize, serialize
from yaml import dump, full_load

from cvp.config.sections.appearance import AppearanceConfig
from cvp.config.sections.concurrency import ConcurrencyConfig
from cvp.config.sections.context import ContextConfig
from cvp.config.sections.developer import DeveloperConfig
from cvp.config.sections.display import DisplayConfig
from cvp.config.sections.ffmpeg import FFmpegConfig
from cvp.config.sections.flow import FlowAuiConfig
from cvp.config.sections.font import FontConfig
from cvp.config.sections.graphic import GraphicConfig
from cvp.config.sections.labeling import LabelingAuiConfig
from cvp.config.sections.layout import LayoutConfig, LayoutManagerConfig
from cvp.config.sections.logging import LoggingConfig
from cvp.config.sections.media import MediaManagerConfig, MediaWindowConfig
from cvp.config.sections.media import Mode as MediaSectionMode
from cvp.config.sections.overlay import OverlayWindowConfig
from cvp.config.sections.preference import PreferenceManagerConfig as PMConfig
from cvp.config.sections.process import ProcessManagerConfig
from cvp.config.sections.stitching import StitchingAuiConfig
from cvp.config.sections.window import WindowManagerConfig
from cvp.config.sections.wsd import WsdConfig, WsdManagerConfig
from cvp.inspect.member import get_public_instance_attributes
from cvp.itertools.find_index import find_index


@dataclass
class Config:
    appearance: AppearanceConfig = field(default_factory=AppearanceConfig)
    concurrency: ConcurrencyConfig = field(default_factory=ConcurrencyConfig)
    context: ContextConfig = field(default_factory=ContextConfig)
    developer: DeveloperConfig = field(default_factory=DeveloperConfig)
    display: DisplayConfig = field(default_factory=DisplayConfig)
    ffmpeg: FFmpegConfig = field(default_factory=FFmpegConfig)
    flow_aui: FlowAuiConfig = field(default_factory=FlowAuiConfig)
    font: FontConfig = field(default_factory=FontConfig)
    graphic: GraphicConfig = field(default_factory=GraphicConfig)
    labeling_aui: LabelingAuiConfig = field(default_factory=LabelingAuiConfig)
    layout_manager: LayoutManagerConfig = field(default_factory=LayoutManagerConfig)
    layouts: List[LayoutConfig] = field(default_factory=list)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    media_manager: MediaManagerConfig = field(default_factory=MediaManagerConfig)
    media_windows: List[MediaWindowConfig] = field(default_factory=list)
    overlay_window: OverlayWindowConfig = field(default_factory=OverlayWindowConfig)
    preference_manager: PMConfig = field(default_factory=PMConfig)
    process_manager: ProcessManagerConfig = field(default_factory=ProcessManagerConfig)
    stitching_aui: StitchingAuiConfig = field(default_factory=StitchingAuiConfig)
    window_manager: WindowManagerConfig = field(default_factory=WindowManagerConfig)
    wsd_manager: WsdManagerConfig = field(default_factory=WsdManagerConfig)
    wsds: List[WsdConfig] = field(default_factory=list)

    @property
    def debug(self):
        return self.developer.debug

    @property
    def verbose(self):
        return self.developer.verbose

    def create_layout(self, name: str, *, append=False):
        config = LayoutConfig(name=name)
        if append:
            self.layouts.append(config)
        return config

    def create_media_file_window(self, file: str, *, opened=False, append=False):
        config = MediaWindowConfig(
            title=os.path.basename(file),
            opened=opened,
            mode=MediaSectionMode.file,
            file=file,
        )
        if append:
            self.media_windows.append(config)
        return config

    def create_media_url_window(self, url: str, *, opened=False, append=False):
        config = MediaWindowConfig(
            title=url,
            opened=opened,
            mode=MediaSectionMode.url,
            file=url,
        )
        if append:
            self.media_windows.append(config)
        return config

    def create_wsd(self, uuid: str, name: str, *, append=False):
        config = WsdConfig(uuid=uuid, name=name)
        if append:
            self.wsds.append(config)
        return config

    def remove_layout(self, uuid: str):
        index = find_index(self.layouts, lambda layout: layout.uuid == uuid)
        if index < 0:
            raise KeyError(f"Not found layout: '{uuid}'")
        return self.layouts.pop(index)

    def remove_media_window(self, uuid: str):
        index = find_index(self.media_windows, lambda mw: mw.uuid == uuid)
        if index < 0:
            raise KeyError(f"Not found media window: '{uuid}'")
        return self.media_windows.pop(index)

    def remove_wsd(self, uuid: str):
        index = find_index(self.wsds, lambda wsd: wsd.uuid == uuid)
        if index < 0:
            raise KeyError(f"Not found wsd: '{uuid}'")
        return self.wsds.pop(index)

    def dumps_yaml(self, encoding="utf-8") -> bytes:
        return dump(serialize(self)).encode(encoding)

    def loads_yaml(self, data: bytes) -> None:
        result = deserialize(full_load(data), type(self))
        assert isinstance(result, type(self))
        attrs = get_public_instance_attributes(self)
        for key, _ in attrs:
            value = getattr(result, key, None)
            if value is not None:
                setattr(self, key, value)

    def write_yaml(self, file: Union[str, PathLike[str]], encoding="utf-8") -> None:
        with open(file, "wb") as f:
            f.write(self.dumps_yaml(encoding))

    def read_yaml(self, file: Union[str, PathLike[str]]) -> None:
        with open(file, "rb") as f:
            self.loads_yaml(f.read())

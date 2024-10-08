# -*- coding: utf-8 -*-

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
from cvp.config.sections.layout import LayoutManagerConfig
from cvp.config.sections.logging import LoggingConfig
from cvp.config.sections.media import MediaManagerConfig, MediaWindowConfig
from cvp.config.sections.overlay import OverlayWindowConfig
from cvp.config.sections.preference import PreferenceManagerConfig as PMConfig
from cvp.config.sections.process import ProcessManagerConfig
from cvp.config.sections.stitching import StitchingAuiConfig
from cvp.config.sections.window import WindowManagerConfig
from cvp.inspect.member import get_public_instance_attributes


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
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    media_manager: MediaManagerConfig = field(default_factory=MediaManagerConfig)
    media_windows: List[MediaWindowConfig] = field(default_factory=list)
    overlay_window: OverlayWindowConfig = field(default_factory=OverlayWindowConfig)
    preference_manager: PMConfig = field(default_factory=PMConfig)
    process_manager: ProcessManagerConfig = field(default_factory=ProcessManagerConfig)
    stitching_aui: StitchingAuiConfig = field(default_factory=StitchingAuiConfig)
    window_manager: WindowManagerConfig = field(default_factory=WindowManagerConfig)

    @property
    def debug(self):
        return self.developer.debug

    @property
    def verbose(self):
        return self.developer.verbose

    def remove_media_window(self, uuid: str) -> None:
        index = -1
        for i, mw in enumerate(self.media_windows):
            if mw.uuid == uuid:
                index = i
                break

        if index < 0:
            raise KeyError(f"Not found media window: '{uuid}'")

        del self.media_windows[index]

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

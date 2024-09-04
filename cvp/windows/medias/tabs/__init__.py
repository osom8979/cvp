# -*- coding: utf-8 -*-

from cvp.config.sections.windows.media import MediaSection
from cvp.widgets.hoc.tab import TabBar
from cvp.windows.medias.tabs.info import MediaInfoTab


class MediaTabs(TabBar[MediaSection]):
    def __init__(self):
        super().__init__()
        self.register(MediaInfoTab())

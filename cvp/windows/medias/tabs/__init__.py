# -*- coding: utf-8 -*-

from cvp.config.sections.media import MediaSection
from cvp.process.manager import ProcessManager
from cvp.widgets.hoc.tab import TabBar
from cvp.windows.medias.tabs.info import MediaInfoTab


class MediaTabs(TabBar[MediaSection]):
    def __init__(self, pm: ProcessManager):
        super().__init__()
        self.register(MediaInfoTab(pm))

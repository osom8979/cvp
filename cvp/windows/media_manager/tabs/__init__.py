# -*- coding: utf-8 -*-

from cvp.config.sections.windows.media import MediaSection
from cvp.context import Context
from cvp.widgets.hoc.tab import TabBar
from cvp.windows.media_manager.tabs.info import MediaInfoTab


class MediaTabs(TabBar[MediaSection]):
    def __init__(self, context: Context):
        super().__init__(context)
        self.register(MediaInfoTab(context))

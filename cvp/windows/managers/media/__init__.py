# -*- coding: utf-8 -*-

from typing import Mapping

from cvp.config.sections.windows.manager.media import MediaManagerSection
from cvp.config.sections.windows.media import MediaSection
from cvp.context import Context
from cvp.types import override
from cvp.widgets.hoc.manager_tab import ManagerTab
from cvp.windows.managers.media.info import MediaInfoTab


class MediaManagerWindow(ManagerTab[MediaManagerSection, MediaSection]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            section=context.config.media_manager,
            title="Media Manager",
            closable=True,
            flags=None,
        )
        self.register(MediaInfoTab(context))

    @override
    def get_menus(self) -> Mapping[str, MediaSection]:
        return self._context.config.media_sections

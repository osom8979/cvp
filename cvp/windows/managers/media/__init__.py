# -*- coding: utf-8 -*-

from collections import OrderedDict

from cvp.config.sections.windows.manager.media import MediaManagerSection
from cvp.config.sections.windows.media import MediaSection
from cvp.context import Context
from cvp.types import override
from cvp.widgets.hoc.manager import ItemsProxy, ManagerWindow
from cvp.windows.managers.media.info import MediaInfoTab


class MediaSectionsProxy(ItemsProxy[MediaSection]):
    def __init__(self, context: Context):
        self._context = context

    @override
    def __call__(self) -> OrderedDict[str, MediaSection]:
        return self._context.config.media_sections


class MediaManagerWindow(ManagerWindow[MediaManagerSection, MediaSection]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            section=context.config.media_manager,
            proxy=MediaSectionsProxy(context),
            title="Media Manager",
            closable=True,
            flags=None,
        )
        self.register(MediaInfoTab(context))

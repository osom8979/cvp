# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import Any, Dict, Generic, Optional, Tuple, TypeVar

import imgui

# noinspection PyProtectedMember
from cvp.config.sections.windows._base import BaseWindowSection
from cvp.context import Context
from cvp.logging.logging import logger
from cvp.types import override
from cvp.variables import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets import set_window_min_size
from cvp.widgets.hoc.popup import Popup
from cvp.widgets.hoc.widget import WidgetInterface

SectionT = TypeVar("SectionT", bound=BaseWindowSection)


class WindowInterface(WidgetInterface):
    @property
    @abstractmethod
    def context(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def key(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def label(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def begin(self) -> Tuple[bool, bool]:
        raise NotImplementedError

    @abstractmethod
    def end(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_create(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_destroy(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_before(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_after(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_popup(self, popup: Popup, result: Any) -> None:
        raise NotImplementedError


class Window(Generic[SectionT], WindowInterface):
    _context: Context
    _popups: Dict[str, Popup]

    def __init__(
        self,
        context: Context,
        section: SectionT,
        title: Optional[str] = None,
        closable: Optional[bool] = None,
        flags: Optional[int] = None,
        min_width=MIN_WINDOW_WIDTH,
        min_height=MIN_WINDOW_HEIGHT,
        modifiable_title=False,
    ) -> None:
        assert isinstance(context, Context)
        assert isinstance(section, BaseWindowSection)

        self._context = context
        self._section = section
        self._title = title if title else type(self).__name__

        if not self._section.has_title:
            self._section.title = self._title

        self.closable = closable if closable else False
        self.flags = flags if flags else 0

        self._min_width = min_width
        self._min_height = min_height
        self._modifiable_title = modifiable_title

        self._initialized = False
        self._popups = dict()

    @property
    def section(self) -> SectionT:
        return self._section

    @property
    def initialized(self) -> bool:
        return self._initialized

    @property
    def opened(self) -> bool:
        return self._section.opened

    @opened.setter
    def opened(self, value: bool) -> None:
        self._section.opened = value

    @property
    def title(self) -> str:
        if self._modifiable_title:
            return self._section.title
        else:
            return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not self._modifiable_title:
            logger.warning(
                f"{repr(self)} "
                "The title of a window that cannot be renamed should not be changed"
            )
        self._section.title = value

    @property
    @override
    def context(self):
        return self._context

    @property
    @override
    def key(self):
        return self.section.section

    @property
    @override
    def label(self) -> str:
        return f"{self.title}###{self.key}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} key={self.key}>"

    def __str__(self) -> str:
        return self.label

    @override
    def begin(self) -> Tuple[bool, bool]:
        expanded, opened = imgui.begin(self.label, self.closable, self.flags)
        assert isinstance(expanded, bool)
        assert isinstance(opened, bool)
        return expanded, opened

    @override
    def end(self) -> None:
        imgui.end()

    @override
    def on_create(self) -> None:
        pass

    @override
    def on_destroy(self) -> None:
        pass

    @override
    def on_before(self) -> None:
        pass

    @override
    def on_process(self) -> None:
        pass

    @override
    def on_after(self) -> None:
        pass

    @override
    def on_popup(self, popup: Popup, result: Any) -> None:
        pass

    def register_popup(self, popup: Popup) -> None:
        self._popups[popup.title] = popup

    def unregister_popup(self, popup: Popup) -> None:
        self._popups.pop(popup.title)

    def do_create(self) -> None:
        if self._initialized:
            raise ValueError("Already initialized")

        self.on_create()
        self._initialized = True

    def do_destroy(self) -> None:
        if not self._initialized:
            raise ValueError("Not initialized")

        self.on_destroy()
        self._initialized = False

    def do_process(self) -> None:
        if not self._initialized:
            raise ValueError("Not initialized")

        if not self.opened:
            return

        self.on_before()

        expanded, opened = self.begin()
        try:
            if imgui.is_window_appearing():
                set_window_min_size(self._min_width, self._min_height)

            if not opened:
                self.opened = False
                return

            if not expanded:
                return

            self.on_process()
        finally:
            self.end()

        for popup in self._popups.values():
            popup_result = popup.do_process()
            if popup_result is not None:
                self.on_popup(popup, popup_result)

        self.on_after()

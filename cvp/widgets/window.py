# -*- coding: utf-8 -*-

from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, Optional, Tuple

import imgui
from pygame.event import Event

from cvp.config.sections import BaseSectionT
from cvp.config.sections.mixins.window import WindowSectionMixin
from cvp.context import Context
from cvp.gui.set_window_min_size import set_window_min_size
from cvp.logging.logging import logger
from cvp.pgc.able.eventable import Eventable
from cvp.pgc.able.keyboardable import Keyboardable
from cvp.pgc.able.mouseable import Mouseable
from cvp.pgc.constants import Constants
from cvp.pgc.constants.event_type import EventType
from cvp.pgc.events.callbacks import EventCallbacks
from cvp.pgc.events.event_map import EventWrapper, create_event_map
from cvp.types import override
from cvp.variables import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets.popup import Popup
from cvp.widgets.widget import WidgetInterface


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
    def on_event(self, event: Event) -> Optional[bool]:
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


@dataclass
class WindowQuery:
    x: float = 0.0
    y: float = 0.0
    w: float = 0.0
    h: float = 0.0

    def update(self):
        self.x, self.y = imgui.get_window_position()
        self.w, self.h = imgui.get_window_size()

    @property
    def position(self):
        return self.x, self.y

    @property
    def size(self):
        return self.w, self.h


class Window(
    Generic[BaseSectionT],
    WindowInterface,
    EventCallbacks,
    Eventable,
    Keyboardable,
    Mouseable,
    Constants,
):
    _context: Context
    _popups: Dict[str, Popup]
    _events: Dict[int, EventWrapper]

    def __init__(
        self,
        context: Context,
        section: BaseSectionT,
        title: Optional[str] = None,
        closable: Optional[bool] = None,
        flags: Optional[int] = None,
        min_width=MIN_WINDOW_WIDTH,
        min_height=MIN_WINDOW_HEIGHT,
        modifiable_title=False,
    ) -> None:
        self._context = context
        self._section = section
        self._title = title if title else type(self).__name__

        if isinstance(self._section, WindowSectionMixin):
            if not self._section.has_title:
                self._section.title = self._title

        self.closable = closable if closable else False
        self.flags = flags if flags else 0

        self._min_width = min_width
        self._min_height = min_height
        self._modifiable_title = modifiable_title

        self._initialized = False
        self._popups = dict()
        self._events = dict()
        self._query = WindowQuery()

    def _has_flag(self, flag: int) -> bool:
        return bool(self.flags & flag)

    def _set_flag(self, flag: int, enable: bool) -> None:
        if enable:
            self.flags |= flag
        else:
            self.flags &= ~flag

    @property
    def no_titlebar(self) -> bool:
        return self._has_flag(imgui.WINDOW_NO_TITLE_BAR)

    @no_titlebar.setter
    def no_titlebar(self, value: bool) -> None:
        self._set_flag(imgui.WINDOW_NO_TITLE_BAR, value)

    @property
    def no_scrollbar(self) -> bool:
        return self._has_flag(imgui.WINDOW_NO_SCROLLBAR)

    @no_scrollbar.setter
    def no_scrollbar(self, value: bool) -> None:
        self._set_flag(imgui.WINDOW_NO_SCROLLBAR, value)

    @property
    def no_menu(self) -> bool:
        return not self._has_flag(imgui.WINDOW_MENU_BAR)

    @no_menu.setter
    def no_menu(self, value: bool) -> None:
        self._set_flag(imgui.WINDOW_MENU_BAR, not value)

    @property
    def no_move(self) -> bool:
        return self._has_flag(imgui.WINDOW_NO_MOVE)

    @no_move.setter
    def no_move(self, value: bool) -> None:
        self._set_flag(imgui.WINDOW_NO_MOVE, value)

    @property
    def no_resize(self) -> bool:
        return self._has_flag(imgui.WINDOW_NO_RESIZE)

    @no_resize.setter
    def no_resize(self, value: bool) -> None:
        self._set_flag(imgui.WINDOW_NO_RESIZE, value)

    @property
    def no_collapse(self) -> bool:
        return self._has_flag(imgui.WINDOW_NO_COLLAPSE)

    @no_collapse.setter
    def no_collapse(self, value: bool) -> None:
        self._set_flag(imgui.WINDOW_NO_COLLAPSE, value)

    @property
    def no_nav(self) -> bool:
        return self._has_flag(imgui.WINDOW_NO_NAV)

    @no_nav.setter
    def no_nav(self, value: bool) -> None:
        self._set_flag(imgui.WINDOW_NO_NAV, value)

    @property
    def no_background(self) -> bool:
        return self._has_flag(imgui.WINDOW_NO_BACKGROUND)

    @no_background.setter
    def no_background(self, value: bool) -> None:
        self._set_flag(imgui.WINDOW_NO_BACKGROUND, value)

    @property
    def no_bring_to_front(self) -> bool:
        return self._has_flag(imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS)

    @no_bring_to_front.setter
    def no_bring_to_front(self, value: bool) -> None:
        self._set_flag(imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS, value)

    @property
    def unsaved_document(self) -> bool:
        return self._has_flag(imgui.WINDOW_UNSAVED_DOCUMENT)

    @unsaved_document.setter
    def unsaved_document(self, value: bool) -> None:
        self._set_flag(imgui.WINDOW_UNSAVED_DOCUMENT, value)

    @property
    def section(self) -> BaseSectionT:
        return self._section

    @property
    def window_section(self) -> WindowSectionMixin:
        assert isinstance(self._section, WindowSectionMixin)
        return self._section

    @property
    def initialized(self) -> bool:
        return self._initialized

    @property
    def opened(self) -> bool:
        return self.window_section.opened

    @opened.setter
    def opened(self, value: bool) -> None:
        self.window_section.opened = value

    @property
    def title(self) -> str:
        if self._modifiable_title:
            return self.window_section.title
        else:
            return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not self._modifiable_title:
            logger.warning(
                f"{repr(self)} "
                "The title of a window that cannot be renamed should not be changed"
            )
        self.window_section.title = value

    @property
    def query(self):
        return self._query

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
    def on_event(self, event: Event) -> Optional[bool]:
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

    def register_event_callback(
        self,
        event_type: EventType,
        callback: Callable,
    ) -> None:
        self._events[event_type].append_callback(callback)

    def update_event_map(self, obj: Any, cls: type) -> None:
        self._events.update(create_event_map(obj, cls))

    def do_create(self) -> None:
        if self._initialized:
            raise ValueError("Already initialized")

        self._events.update(create_event_map(self))
        self.on_create()
        self._initialized = True

    def do_destroy(self) -> None:
        if not self._initialized:
            raise ValueError("Not initialized")

        self.on_destroy()
        self._events.clear()
        self._initialized = False

    def do_event(self, event: Event) -> Optional[bool]:
        if bool(self.on_event(event)):
            return True

        return self._events[event.type](event)

    def do_process(self) -> None:
        if not self._initialized:
            raise ValueError("Not initialized")

        if not self.opened:
            return

        self.on_before()

        expanded, opened = self.begin()
        try:
            self._query.update()

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
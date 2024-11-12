# -*- coding: utf-8 -*-

from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, Optional, Tuple, TypeVar

import imgui
from pygame.event import Event

from cvp.config.sections.bases.window import WindowConfig
from cvp.context.context import Context
from cvp.imgui.set_window_min_size import set_window_min_size
from cvp.logging.logging import logger
from cvp.msgs.callbacks import MsgCallbacks
from cvp.msgs.msg import Msg
from cvp.msgs.msg_map import MsgWrapper, create_msg_map
from cvp.msgs.msg_type import MsgTypeLike, get_msg_type_number
from cvp.pygame.able.eventable import Eventable
from cvp.pygame.able.keyboardable import Keyboardable
from cvp.pygame.able.mouseable import Mouseable
from cvp.pygame.constants import Constants
from cvp.pygame.constants.event_type import EventType
from cvp.pygame.events.callbacks import EventCallbacks
from cvp.pygame.events.event_map import EventWrapper, create_event_map
from cvp.renderer.popup.popup import Popup
from cvp.renderer.window.widget import WidgetInterface
from cvp.types.override import override
from cvp.variables import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH


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
    def on_msg(self, msg: Msg) -> Optional[bool]:
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


WindowConfigT = TypeVar("WindowConfigT", bound=WindowConfig)


@dataclass
class WindowQuery:
    x: float = 0.0
    y: float = 0.0
    w: float = 0.0
    h: float = 0.0
    focused: bool = False
    hovered: bool = False

    def update(self):
        self.x, self.y = imgui.get_window_position()
        self.w, self.h = imgui.get_window_size()
        self.focused = imgui.is_window_focused()
        self.hovered = imgui.is_window_hovered()

    @property
    def position(self):
        return self.x, self.y

    @property
    def size(self):
        return self.w, self.h


class Window(
    Generic[WindowConfigT],
    WindowInterface,
    EventCallbacks,
    MsgCallbacks,
    Eventable,
    Keyboardable,
    Mouseable,
    Constants,
):
    _popups: Dict[str, Popup]
    _events: Dict[int, EventWrapper]
    _msgs: Dict[int, MsgWrapper]

    def __init__(
        self,
        context: Context,
        window_config: WindowConfigT,
        title: Optional[str] = None,
        closable: Optional[bool] = None,
        flags: Optional[int] = None,
        min_width=MIN_WINDOW_WIDTH,
        min_height=MIN_WINDOW_HEIGHT,
        modifiable_title=False,
    ) -> None:
        self._context = context
        self._window_config = window_config
        self._title = title if title else type(self).__name__

        if not self._window_config.title:
            self._window_config.title = self._title

        self.closable = closable if closable else False
        self.flags = flags if flags else 0

        self._min_width = min_width
        self._min_height = min_height
        self._modifiable_title = modifiable_title

        self._initialized = False
        self._removable = False
        self._popups = dict()
        self._events = dict()
        self._msgs = dict()
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
    def window_config(self):
        return self._window_config

    @property
    def initialized(self) -> bool:
        return self._initialized

    @property
    def removable(self) -> bool:
        return self._removable

    def set_removable(self) -> None:
        self._removable = True
        logger.debug(
            f"{repr(self)} "
            "The 'removable' flag is enabled. "
            "The destroy event is called just before the next loop execution."
        )

    @property
    def opened(self) -> bool:
        return self._window_config.opened

    @opened.setter
    def opened(self, value: bool) -> None:
        self._window_config.opened = value

    def flip_opened(self) -> None:
        self._window_config.opened = not self._window_config.opened

    @property
    def title(self) -> str:
        if self._modifiable_title:
            return self._window_config.title
        else:
            return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not self._modifiable_title:
            logger.warning(
                f"{repr(self)} "
                "The title of a window that cannot be renamed should not be changed"
            )
        self._window_config.title = value

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
        return self.window_config.uuid

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
    def on_msg(self, msg: Msg) -> Optional[bool]:
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

    def register_msg_callback(self, msg_type: MsgTypeLike, callback: Callable) -> None:
        self._msgs[get_msg_type_number(msg_type)].append_callback(callback)

    def update_event_map(self, obj: Any, cls: type) -> None:
        self._events.update(create_event_map(obj, cls))

    def update_msg_map(self, obj: Any, cls: type) -> None:
        self._msgs.update(create_msg_map(obj, cls))

    def do_create(self) -> None:
        if self._initialized:
            raise ValueError("Already initialized window instance")

        self._events.update(create_event_map(self))
        self._msgs.update(create_msg_map(self))

        try:
            self.on_create()
        except BaseException as e:
            logger.error(f"{repr(self)} {e}")
            raise e

        self._initialized = True
        logger.info(f"{repr(self)} The constructor has been called")

    def do_destroy(self) -> None:
        if not self._initialized:
            raise ValueError("The window instance is not initialized")

        try:
            self.on_destroy()
        except BaseException as e:
            logger.error(f"{repr(self)} {e}")
            raise e

        self._events.clear()
        self._initialized = False
        logger.info(f"{repr(self)} The destructor has been called")

    def do_event(self, event: Event) -> Optional[bool]:
        if not self._initialized:
            raise ValueError("The window instance is not initialized")

        if bool(self.on_event(event)):
            return True

        return self._events[event.type](event)

    def do_msg(self, msg: Msg) -> Optional[bool]:
        if not self._initialized:
            raise ValueError("The window instance is not initialized")

        if bool(self.on_msg(msg)):
            return True

        return self._msgs[get_msg_type_number(msg.type)](msg)

    def do_process(self) -> None:
        if not self._initialized:
            raise ValueError("The window instance is not initialized")

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

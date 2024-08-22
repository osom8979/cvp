# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, Tuple, TypeVar

import imgui

from cvp.config.sections.commons.window import CommonWindowSection
from cvp.types.override import override
from cvp.variables import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets import set_window_min_size
from cvp.widgets.hoc.popup import Popup

SectionT = TypeVar("SectionT", bound=CommonWindowSection)


class WindowInterface(ABC):
    @abstractmethod
    def get_title(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_closable(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_flags(self) -> int:
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
    def on_process(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_after(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_popup(self, popup: Popup, result: Any) -> None:
        pass


class Window(Generic[SectionT], WindowInterface):
    _popups: Dict[str, Popup]

    def __init__(
        self,
        section: SectionT,
        title: Optional[str] = None,
        closable: Optional[bool] = None,
        flags: Optional[int] = None,
        min_width=MIN_WINDOW_WIDTH,
        min_height=MIN_WINDOW_HEIGHT,
    ) -> None:
        assert isinstance(section, CommonWindowSection)
        self._section = section
        self._title = title
        self._closable = closable
        self._flags = flags
        self._min_width = min_width
        self._min_height = min_height
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

    @override
    def get_title(self) -> str:
        return self._title if self._title else type(self).__name__

    @override
    def get_closable(self) -> bool:
        return self._closable if self._closable else False

    @override
    def get_flags(self) -> int:
        return self._flags if self._flags else 0

    @override
    def begin(self) -> Tuple[bool, bool]:
        expanded, opened = imgui.begin(
            self.get_title(),
            self.get_closable(),
            self.get_flags(),
        )
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
            return

        self.on_create()
        self._initialized = True

    def do_destroy(self) -> None:
        if not self._initialized:
            return

        self.on_destroy()
        self._initialized = False

    def do_process(self) -> None:
        if not self._initialized:
            self.on_create()
            self._initialized = True

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

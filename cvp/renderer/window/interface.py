# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import Any, Optional, Tuple

from pygame import Event

from cvp.msgs.msg import Msg
from cvp.renderer.popup.base import PopupBase
from cvp.renderer.widget.interface import WidgetInterface


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
    def on_appearing(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_disappeared(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_focused(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_unfocused(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_hovered(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_unhovered(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_shown(self):
        raise NotImplementedError

    @abstractmethod
    def on_hidden(self):
        raise NotImplementedError

    @abstractmethod
    def on_expanded(self):
        raise NotImplementedError

    @abstractmethod
    def on_unexpanded(self):
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
    def on_popup(self, popup: PopupBase, result: Any) -> None:
        raise NotImplementedError

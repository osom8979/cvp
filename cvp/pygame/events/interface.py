# -*- coding: utf-8 -*-

from abc import ABCMeta
from typing import Optional, Tuple

from cvp.pygame.constants.button_type import ButtonType
from cvp.pygame.constants.keycode import Keycode
from cvp.pygame.constants.keymod import Keymod
from cvp.pygame.events.abc import abstractevent
from pygame import constants


class EventInterface(metaclass=ABCMeta):
    @abstractevent(constants.QUIT)
    def on_quit(self) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.ACTIVEEVENT)
    def on_active_event(self, gain: int, state: int) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.KEYDOWN)
    def on_key_down(
        self,
        key: Keycode,
        mod: Keymod,
        unicode: str,
        scancode: int,
    ) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.KEYUP)
    def on_key_up(
        self,
        key: Keycode,
        mod: Keymod,
        unicode: str,
        scancode: int,
    ) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.MOUSEMOTION)
    def on_mouse_motion(
        self,
        pos: Tuple[int, int],
        rel: Tuple[int, int],
        buttons: Tuple[int, int, int],
        touch: bool,
    ) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.MOUSEBUTTONUP)
    def on_mouse_button_up(
        self,
        pos: Tuple[int, int],
        button: ButtonType,
        touch: bool,
    ) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.MOUSEBUTTONDOWN)
    def on_mouse_button_down(
        self,
        pos: Tuple[int, int],
        button: ButtonType,
        touch: bool,
    ) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.JOYAXISMOTION)
    def on_joy_axis_motion(self, joy, instance_id, axis, value) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.JOYBALLMOTION)
    def on_joy_ball_motion(self, joy, instance_id, ball, rel) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.JOYHATMOTION)
    def on_joy_hat_motion(self, joy, instance_id, hat, value) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.JOYBUTTONUP)
    def on_joy_button_up(self, joy, instance_id, button) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.JOYBUTTONDOWN)
    def on_joy_button_down(self, joy, instance_id, button) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.VIDEORESIZE)
    def on_video_resize(self, size: Tuple[int, int], w: int, h: int) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.VIDEOEXPOSE)
    def on_video_expose(self) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.USEREVENT)
    def on_user_event(self, code: int) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.AUDIODEVICEADDED)
    def on_audio_device_added(self, which: int, iscapture: int) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.AUDIODEVICEREMOVED)
    def on_audio_device_removed(self, which: int, iscapture: int) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.FINGERMOTION)
    def on_finger_motion(self, touch_id, finger_id, x, y, dx, dy) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.FINGERDOWN)
    def on_finger_down(self, touch_id, finger_id, x, y, dx, dy) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.FINGERUP)
    def on_finger_up(self, touch_id, finger_id, x, y, dx, dy) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.MOUSEWHEEL)
    def on_mouse_wheel(
        self,
        flipped: bool,
        x: int,
        y: int,
        precise_x: float,
        precise_y: float,
        touch: bool,
    ) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.MULTIGESTURE)
    def on_multi_gesture(
        self,
        touch_id,
        x,
        y,
        pinched,
        rotated,
        num_fingers,
    ) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.TEXTEDITING)
    def on_text_editing(self, text: str, start: int, length: int) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.TEXTINPUT)
    def on_text_input(self, text: str) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.DROPFILE)
    def on_drop_file(self, file: str) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.DROPBEGIN)
    def on_drop_begin(self) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.DROPCOMPLETE)
    def on_drop_complete(self) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.DROPTEXT)
    def on_drop_text(self) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.MIDIIN)
    def on_midi_in(self) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.MIDIOUT)
    def on_midi_out(self) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.CONTROLLERDEVICEADDED)
    def on_controller_device_added(self, device_index: int) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.JOYDEVICEADDED)
    def on_joy_device_added(self, device_index: int) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.CONTROLLERDEVICEREMOVED)
    def on_controller_device_removed(self, instance_id: int) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.JOYDEVICEREMOVED)
    def on_joy_device_removed(self, instance_id: int) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.CONTROLLERDEVICEREMAPPED)
    def on_controller_device_remapped(self, instance_id: int) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.KEYMAPCHANGED)
    def on_keymap_changed(self) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.CLIPBOARDUPDATE)
    def on_clipboard_update(self) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.RENDER_TARGETS_RESET)
    def on_render_targets_reset(self) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.RENDER_DEVICE_RESET)
    def on_render_device_reset(self) -> Optional[bool]:
        raise NotImplementedError

    @abstractevent(constants.LOCALECHANGED)
    def on_locale_changed(self) -> Optional[bool]:
        """[PyGame 2] (SDL backend >= 2.0.14)"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWSHOWN)
    def on_window_shown(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window became shown"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWHIDDEN)
    def on_window_hidden(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window became hidden"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWEXPOSED)
    def on_window_exposed(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window got updated by some external event"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWMOVED)
    def on_window_moved(self, x: int, y: int) -> Optional[bool]:
        """[PyGame 2.0.1] Window got moved"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWRESIZED)
    def on_window_resized(self, x: int, y: int) -> Optional[bool]:
        """[PyGame 2.0.1] Window got resized"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWSIZECHANGED)
    def on_window_size_changed(self, x: int, y: int) -> Optional[bool]:
        """[PyGame 2.0.1] Window changed its size"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWMINIMIZED)
    def on_window_minimized(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window was minimized"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWMAXIMIZED)
    def on_window_maximized(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window was maximized"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWRESTORED)
    def on_window_restored(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window was restored"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWENTER)
    def on_window_enter(self) -> Optional[bool]:
        """[PyGame 2.0.1] Mouse entered the window"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWLEAVE)
    def on_window_leave(self) -> Optional[bool]:
        """[PyGame 2.0.1] Mouse left the window"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWFOCUSGAINED)
    def on_window_focus_gained(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window gained focus"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWFOCUSLOST)
    def on_window_focus_lost(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window lost focus"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWCLOSE)
    def on_window_close(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window was closed"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWTAKEFOCUS)
    def on_window_take_focus(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window was offered focus"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWHITTEST)
    def on_window_hit_test(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window has a special hit test"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWICCPROFCHANGED)
    def on_window_icc_prof_changed(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window ICC profile changed (SDL backend >= 2.0.18)"""
        raise NotImplementedError

    @abstractevent(constants.WINDOWDISPLAYCHANGED)
    def on_window_display_changed(self) -> Optional[bool]:
        """[PyGame 2.0.1] Window moved on a new display (SDL backend >= 2.0.18)"""
        raise NotImplementedError

    @abstractevent(constants.APP_TERMINATING)
    def on_app_terminating(self) -> Optional[bool]:
        """[Android] OS is terminating the application"""
        raise NotImplementedError

    @abstractevent(constants.APP_LOWMEMORY)
    def on_app_low_memory(self) -> Optional[bool]:
        """[Android] OS is low on memory, try to free memory if possible"""
        raise NotImplementedError

    @abstractevent(constants.APP_WILLENTERBACKGROUND)
    def on_app_will_enter_background(self) -> Optional[bool]:
        """[Android] Application is entering background"""
        raise NotImplementedError

    @abstractevent(constants.APP_DIDENTERBACKGROUND)
    def on_app_did_enter_background(self) -> Optional[bool]:
        """[Android] Application entered background"""
        raise NotImplementedError

    @abstractevent(constants.APP_WILLENTERFOREGROUND)
    def on_app_will_enter_foreground(self) -> Optional[bool]:
        """[Android] Application is entering foreground"""
        raise NotImplementedError

    @abstractevent(constants.APP_DIDENTERFOREGROUND)
    def on_app_did_enter_foreground(self) -> Optional[bool]:
        """[Android] Application entered foreground"""
        raise NotImplementedError
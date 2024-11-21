# -*- coding: utf-8 -*-

from typing import Tuple

from cvp.pygame.constants.button_type import ButtonType
from cvp.pygame.constants.keycode import Keycode
from cvp.pygame.constants.keymod import Keymod
from cvp.pygame.events.interface import EventInterface
from cvp.types.override import override


class EventCallbacks(EventInterface):
    @override
    def on_quit(self):
        pass

    @override
    def on_active_event(self, gain: int, state: int):
        pass

    @override
    def on_key_down(
        self,
        key: Keycode,
        mod: Keymod,
        unicode: str,
        scancode: int,
    ):
        pass

    @override
    def on_key_up(
        self,
        key: Keycode,
        mod: Keymod,
        unicode: str,
        scancode: int,
    ):
        pass

    @override
    def on_mouse_motion(
        self,
        pos: Tuple[int, int],
        rel: Tuple[int, int],
        buttons: Tuple[int, int, int],
        touch: bool,
    ):
        pass

    @override
    def on_mouse_button_up(
        self,
        pos: Tuple[int, int],
        button: ButtonType,
        touch: bool,
    ):
        pass

    @override
    def on_mouse_button_down(
        self,
        pos: Tuple[int, int],
        button: ButtonType,
        touch: bool,
    ):
        pass

    @override
    def on_joy_axis_motion(self, joy, instance_id, axis, value):
        pass

    @override
    def on_joy_ball_motion(self, joy, instance_id, ball, rel):
        pass

    @override
    def on_joy_hat_motion(self, joy, instance_id, hat, value):
        pass

    @override
    def on_joy_button_up(self, joy, instance_id, button):
        pass

    @override
    def on_joy_button_down(self, joy, instance_id, button):
        pass

    @override
    def on_video_resize(self, size: Tuple[int, int], w: int, h: int):
        pass

    @override
    def on_video_expose(self):
        pass

    @override
    def on_user_event(self, code: int):
        pass

    @override
    def on_audio_device_added(self, which: int, iscapture: int):
        pass

    @override
    def on_audio_device_removed(self, which: int, iscapture: int):
        pass

    @override
    def on_finger_motion(self, touch_id, finger_id, x, y, dx, dy):
        pass

    @override
    def on_finger_down(self, touch_id, finger_id, x, y, dx, dy):
        pass

    @override
    def on_finger_up(self, touch_id, finger_id, x, y, dx, dy):
        pass

    @override
    def on_mouse_wheel(
        self,
        flipped: bool,
        x: int,
        y: int,
        precise_x: float,
        precise_y: float,
        touch: bool,
    ):
        pass

    @override
    def on_multi_gesture(
        self,
        touch_id,
        x,
        y,
        pinched,
        rotated,
        num_fingers,
    ):
        pass

    @override
    def on_text_editing(self, text: str, start: int, length: int):
        pass

    @override
    def on_text_input(self, text: str):
        pass

    @override
    def on_drop_file(self, file: str):
        pass

    @override
    def on_drop_begin(self):
        pass

    @override
    def on_drop_complete(self):
        pass

    @override
    def on_drop_text(self):
        pass

    @override
    def on_midi_in(self):
        pass

    @override
    def on_midi_out(self):
        pass

    @override
    def on_controller_device_added(self, device_index: int):
        pass

    @override
    def on_joy_device_added(self, device_index: int):
        pass

    @override
    def on_controller_device_removed(self, instance_id: int):
        pass

    @override
    def on_joy_device_removed(self, instance_id: int):
        pass

    @override
    def on_controller_device_remapped(self, instance_id: int):
        pass

    @override
    def on_keymap_changed(self):
        pass

    @override
    def on_clipboard_update(self):
        pass

    @override
    def on_render_targets_reset(self):
        pass

    @override
    def on_render_device_reset(self):
        pass

    @override
    def on_locale_changed(self):
        pass

    @override
    def on_window_shown(self):
        pass

    @override
    def on_window_hidden(self):
        pass

    @override
    def on_window_exposed(self):
        pass

    @override
    def on_window_moved(self, x: int, y: int):
        pass

    @override
    def on_window_resized(self, x: int, y: int):
        pass

    @override
    def on_window_size_changed(self, x: int, y: int):
        pass

    @override
    def on_window_minimized(self):
        pass

    @override
    def on_window_maximized(self):
        pass

    @override
    def on_window_restored(self):
        pass

    @override
    def on_window_enter(self):
        pass

    @override
    def on_window_leave(self):
        pass

    @override
    def on_window_focus_gained(self):
        pass

    @override
    def on_window_focus_lost(self):
        pass

    @override
    def on_window_close(self):
        pass

    @override
    def on_window_take_focus(self):
        pass

    @override
    def on_window_hit_test(self):
        pass

    @override
    def on_window_icc_prof_changed(self):
        pass

    @override
    def on_window_display_changed(self):
        pass

    @override
    def on_app_terminating(self):
        pass

    @override
    def on_app_low_memory(self):
        pass

    @override
    def on_app_will_enter_background(self):
        pass

    @override
    def on_app_did_enter_background(self):
        pass

    @override
    def on_app_will_enter_foreground(self):
        pass

    @override
    def on_app_did_enter_foreground(self):
        pass

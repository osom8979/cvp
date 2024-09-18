# -*- coding: utf-8 -*-

from typing import Optional, Tuple

from overrides import override

from cvp.renderer.pygame.constants.button_type import ButtonType
from cvp.renderer.pygame.constants.keycode import Keycode
from cvp.renderer.pygame.constants.keymod import Keymod
from cvp.renderer.pygame.events.interface import EventInterface


class EventCallbacks(EventInterface):
    @override
    def on_quit(self) -> Optional[bool]:
        pass

    @override
    def on_active_event(self, gain: int, state: int) -> Optional[bool]:
        pass

    @override
    def on_key_down(
        self,
        key: Keycode,
        mod: Keymod,
        unicode: str,
        scancode: int,
    ) -> Optional[bool]:
        pass

    @override
    def on_key_up(
        self,
        key: Keycode,
        mod: Keymod,
        unicode: str,
        scancode: int,
    ) -> Optional[bool]:
        pass

    @override
    def on_mouse_motion(
        self,
        pos: Tuple[int, int],
        rel: Tuple[int, int],
        buttons: Tuple[int, int, int],
        touch: bool,
    ) -> Optional[bool]:
        pass

    @override
    def on_mouse_button_up(
        self,
        pos: Tuple[int, int],
        button: ButtonType,
        touch: bool,
    ) -> Optional[bool]:
        pass

    @override
    def on_mouse_button_down(
        self,
        pos: Tuple[int, int],
        button: ButtonType,
        touch: bool,
    ) -> Optional[bool]:
        pass

    @override
    def on_joy_axis_motion(self, joy, instance_id, axis, value) -> Optional[bool]:
        pass

    @override
    def on_joy_ball_motion(self, joy, instance_id, ball, rel) -> Optional[bool]:
        pass

    @override
    def on_joy_hat_motion(self, joy, instance_id, hat, value) -> Optional[bool]:
        pass

    @override
    def on_joy_button_up(self, joy, instance_id, button) -> Optional[bool]:
        pass

    @override
    def on_joy_button_down(self, joy, instance_id, button) -> Optional[bool]:
        pass

    @override
    def on_video_resize(self, size: Tuple[int, int], w: int, h: int) -> Optional[bool]:
        pass

    @override
    def on_video_expose(self) -> Optional[bool]:
        pass

    @override
    def on_user_event(self, code: int) -> Optional[bool]:
        pass

    @override
    def on_audio_device_added(self, which: int, iscapture: int) -> Optional[bool]:
        pass

    @override
    def on_audio_device_removed(self, which: int, iscapture: int) -> Optional[bool]:
        pass

    @override
    def on_finger_motion(self, touch_id, finger_id, x, y, dx, dy) -> Optional[bool]:
        pass

    @override
    def on_finger_down(self, touch_id, finger_id, x, y, dx, dy) -> Optional[bool]:
        pass

    @override
    def on_finger_up(self, touch_id, finger_id, x, y, dx, dy) -> Optional[bool]:
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
    ) -> Optional[bool]:
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
    ) -> Optional[bool]:
        pass

    @override
    def on_text_editing(self, text: str, start: int, length: int) -> Optional[bool]:
        pass

    @override
    def on_text_input(self, text: str) -> Optional[bool]:
        pass

    @override
    def on_drop_file(self, file: str) -> Optional[bool]:
        pass

    @override
    def on_drop_begin(self) -> Optional[bool]:
        pass

    @override
    def on_drop_complete(self) -> Optional[bool]:
        pass

    @override
    def on_drop_text(self) -> Optional[bool]:
        pass

    @override
    def on_midi_in(self) -> Optional[bool]:
        pass

    @override
    def on_midi_out(self) -> Optional[bool]:
        pass

    @override
    def on_controller_device_added(self, device_index: int) -> Optional[bool]:
        pass

    @override
    def on_joy_device_added(self, device_index: int) -> Optional[bool]:
        pass

    @override
    def on_controller_device_removed(self, instance_id: int) -> Optional[bool]:
        pass

    @override
    def on_joy_device_removed(self, instance_id: int) -> Optional[bool]:
        pass

    @override
    def on_controller_device_remapped(self, instance_id: int) -> Optional[bool]:
        pass

    @override
    def on_keymap_changed(self) -> Optional[bool]:
        pass

    @override
    def on_clipboard_update(self) -> Optional[bool]:
        pass

    @override
    def on_render_targets_reset(self) -> Optional[bool]:
        pass

    @override
    def on_render_device_reset(self) -> Optional[bool]:
        pass

    @override
    def on_locale_changed(self) -> Optional[bool]:
        pass

    @override
    def on_window_shown(self) -> Optional[bool]:
        pass

    @override
    def on_window_hidden(self) -> Optional[bool]:
        pass

    @override
    def on_window_exposed(self) -> Optional[bool]:
        pass

    @override
    def on_window_moved(self, x: int, y: int) -> Optional[bool]:
        pass

    @override
    def on_window_resized(self, x: int, y: int) -> Optional[bool]:
        pass

    @override
    def on_window_size_changed(self, x: int, y: int) -> Optional[bool]:
        pass

    @override
    def on_window_minimized(self) -> Optional[bool]:
        pass

    @override
    def on_window_maximized(self) -> Optional[bool]:
        pass

    @override
    def on_window_restored(self) -> Optional[bool]:
        pass

    @override
    def on_window_enter(self) -> Optional[bool]:
        pass

    @override
    def on_window_leave(self) -> Optional[bool]:
        pass

    @override
    def on_window_focus_gained(self) -> Optional[bool]:
        pass

    @override
    def on_window_focus_lost(self) -> Optional[bool]:
        pass

    @override
    def on_window_close(self) -> Optional[bool]:
        pass

    @override
    def on_window_take_focus(self) -> Optional[bool]:
        pass

    @override
    def on_window_hit_test(self) -> Optional[bool]:
        pass

    @override
    def on_window_icc_prof_changed(self) -> Optional[bool]:
        pass

    @override
    def on_window_display_changed(self) -> Optional[bool]:
        pass

    @override
    def on_app_terminating(self) -> Optional[bool]:
        pass

    @override
    def on_app_low_memory(self) -> Optional[bool]:
        pass

    @override
    def on_app_will_enter_background(self) -> Optional[bool]:
        pass

    @override
    def on_app_did_enter_background(self) -> Optional[bool]:
        pass

    @override
    def on_app_will_enter_foreground(self) -> Optional[bool]:
        pass

    @override
    def on_app_did_enter_foreground(self) -> Optional[bool]:
        pass

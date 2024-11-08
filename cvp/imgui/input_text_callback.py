# -*- coding: utf-8 -*-

import imgui

# noinspection PyProtectedMember
from imgui.core import _ImGuiInputTextCallbackData


class InputTextCallback:
    def __call__(self, data: _ImGuiInputTextCallbackData) -> int:
        io = imgui.get_io()

        if not io.key_ctrl:
            return 0

        if imgui.is_key_pressed(imgui.core.KEY_C):
            if data.has_selection():
                begin = data.selection_start
                end = data.selection_end
                selected_text = data.buffer[begin:end]
                imgui.set_clipboard_text(selected_text)
            return 0

        if imgui.is_key_pressed(imgui.core.KEY_V):
            clipboard_text = imgui.get_clipboard_text()
            if clipboard_text:

                if data.has_selection():
                    begin = data.selection_start
                    end = data.selection_end
                    data.delete_chars(begin, end - begin)
                    data.cursor_pos = begin

                data.insert_chars(data.cursor_pos, clipboard_text)

        return 0

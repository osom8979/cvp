# -*- coding: utf-8 -*-

import imgui

from cvp.context import Context
from cvp.types import override
from cvp.widgets import button_ex, checkbox, input_text_disabled
from cvp.widgets.hoc.tab import TabItem
from cvp.widgets.hoc.window import Window


class WindowInfoTab(TabItem[Window]):
    def __init__(self, context: Context):
        super().__init__(context, "Info")

    @override
    def on_item(self, item: Window) -> None:
        imgui.text("Key:")
        input_text_disabled("## Label", item.key)

        imgui.text("Title:")
        input_text_disabled("## Title", item.title)

        imgui.text("Label:")
        input_text_disabled("## Label", item.label)

        imgui.separator()
        imgui.text("Visibility:")

        if button_ex("Show", disabled=item.opened):
            item.opened = True
        imgui.same_line()
        if button_ex("Hide", disabled=not item.opened):
            item.opened = False

        # imgui.separator()
        # imgui.text("Geometry:")
        #
        # imgui.push_id(item.label)
        # try:
        #     cx, cy = imgui.get_window_position()
        #     cw, ch = imgui.get_window_size()
        # finally:
        #     imgui.pop_id()
        #
        # pos_result = imgui.drag_float2("Position", cx, cy)
        # if pos_result[0]:
        #     pos_value = pos_result[1]
        #     x = pos_value[0]
        #     y = pos_value[1]
        #     imgui.push_id(item.label)
        #     try:
        #         imgui.set_window_size(x, y)
        #     finally:
        #         imgui.pop_id()
        #
        # size_result = imgui.drag_float2("Size", cw, ch)
        # if size_result[0]:
        #     size_value = size_result[1]
        #     w = size_value[0]
        #     h = size_value[1]
        #     imgui.push_id(item.label)
        #     try:
        #         imgui.set_window_size(w, h)
        #     finally:
        #         imgui.pop_id()

        imgui.separator()
        imgui.text("Options:")

        with imgui.begin_table("## OptionsTable", 3):
            imgui.table_next_column()
            if cb_result := checkbox("No titlebar", item.no_titlebar):
                item.no_titlebar = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No scrollbar", item.no_scrollbar):
                item.no_scrollbar = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No menu", item.no_menu):
                item.no_menu = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No move", item.no_move):
                item.no_move = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No resize", item.no_resize):
                item.no_resize = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No collapse", item.no_collapse):
                item.no_collapse = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("Closable", item.closable):
                item.closable = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No nav", item.no_nav):
                item.no_nav = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No background", item.no_background):
                item.no_background = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No bring to front", item.no_bring_to_front):
                item.no_bring_to_front = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("Unsaved document", item.unsaved_document):
                item.unsaved_document = cb_result.state

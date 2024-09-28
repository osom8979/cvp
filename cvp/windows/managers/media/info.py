# -*- coding: utf-8 -*-

import imgui

from cvp.config.sections.media_window import MediaWindowSection
from cvp.context import Context
from cvp.ffmpeg.ffprobe.inspect import inspect_video_frame_size
from cvp.gui.button_ex import button_ex
from cvp.gui.input_text_disabled import input_text_disabled
from cvp.gui.input_text_value import input_text_value
from cvp.gui.item_width import item_width
from cvp.logging.logging import logger
from cvp.types import override
from cvp.widgets.tab import TabItem


class MediaInfoTab(TabItem[MediaWindowSection]):
    def __init__(self, context: Context):
        super().__init__(context, "Info")

    @override
    def on_item(self, item: MediaWindowSection) -> None:
        imgui.text("Section:")
        input_text_disabled("## Section", item.section)

        imgui.text("Title:")
        with item_width(-1):
            item.title = input_text_value("## Title", item.title)

        imgui.text("File:")
        with item_width(-1):
            item.file = input_text_value("## File", item.file)

        spawnable = self.context.pm.spawnable(item.section)
        stoppable = self.context.pm.stoppable(item.section)
        removable = self.context.pm.removable(item.section)

        imgui.separator()
        imgui.text("Frame:")
        item.frame_size = imgui.input_int2("Size", *item.frame_size)[1]
        if imgui.button("Reset"):
            item.frame_size = 0, 0
        imgui.same_line()
        if imgui.button("Inspect"):
            try:
                item.frame_size = inspect_video_frame_size(item.file)
            except BaseException as e:
                logger.error(e)

        imgui.separator()
        status = self.context.pm.status(item.section)
        imgui.text(f"Process ({status})")

        if button_ex("Spawn", disabled=not spawnable):
            self.context.pm.spawn_ffmpeg_with_file(
                key=item.section,
                file=item.file,
                width=item.frame_width,
                height=item.frame_height,
            )
        imgui.same_line()
        if button_ex("Stop", disabled=not stoppable):
            self.context.pm.interrupt(item.section)
        imgui.same_line()
        if button_ex("Remove", disabled=not removable):
            self.context.pm.pop(item.section)

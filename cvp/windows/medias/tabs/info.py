# -*- coding: utf-8 -*-

from typing import Optional
from weakref import ref

import imgui

from cvp.config.sections.windows.media import MediaSection
from cvp.ffmpeg.ffprobe.inspect import inspect_video_frame_size
from cvp.process.manager import ProcessManager
from cvp.types import override
from cvp.widgets import (
    button_ex,
    input_text_disabled,
    input_text_value,
    item_width,
    text_centered,
)
from cvp.widgets.hoc.tab import TabItem


class MediaInfoTab(TabItem[MediaSection]):
    def __init__(self, pm: ProcessManager):
        super().__init__("Info")
        self._pm = ref(pm)

    @property
    def pm(self) -> Optional[ProcessManager]:
        return self._pm()

    @override
    def on_context(self, context: MediaSection) -> None:
        pm = self.pm
        if pm is None:
            text_centered("ProcessManager reference is dead")
            return

        imgui.text("Section:")
        input_text_disabled("## Section", context.section)

        imgui.text("Name:")
        with item_width(-1):
            context.name = input_text_value("## Name", context.name)

        imgui.text("File:")
        with item_width(-1):
            context.file = input_text_value("## File", context.file)

        spawnable = pm.spawnable(context.section)
        stoppable = pm.stoppable(context.section)
        removable = pm.removable(context.section)

        imgui.separator()
        imgui.text("Frame:")
        context.frame_size = imgui.input_int2("Size", *context.frame_size)[1]
        if imgui.button("Reset"):
            context.frame_size = 0, 0
        imgui.same_line()
        if imgui.button("Inspect"):
            try:
                context.frame_size = inspect_video_frame_size(context.file)
            except BaseException as e:
                print(e)

        imgui.separator()
        status = pm.status(context.section)
        imgui.text(f"Process ({status})")

        if button_ex("Spawn", disabled=not spawnable):
            pm.spawn_ffmpeg_with_file(
                key=context.section,
                file=context.file,
                width=context.frame_width,
                height=context.frame_height,
            )
        imgui.same_line()
        if button_ex("Stop", disabled=not stoppable):
            pm.interrupt(context.section)
        imgui.same_line()
        if button_ex("Remove", disabled=not removable):
            pm.pop(context.section)

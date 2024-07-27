# -*- coding: utf-8 -*-

from typing import Final, Optional

import imgui
from overrides import override

from cvp.apps.player.config.root import RootConfig
from cvp.apps.player.interface import WindowInterface
from cvp.images.load import TextureTuple

BACKGROUND_WINDOW_FLAGS: Final[int] = (
    imgui.WINDOW_NO_DECORATION
    | imgui.WINDOW_NO_SAVED_SETTINGS
    | imgui.WINDOW_NO_FOCUS_ON_APPEARING
    | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
    | imgui.WINDOW_NO_NAV
    | imgui.WINDOW_NO_MOVE
)


class BackgroundWindow(WindowInterface):
    _logo_texture: Optional[TextureTuple]

    def __init__(self, config: RootConfig, flags=BACKGROUND_WINDOW_FLAGS):
        self._config = config
        self._flags = flags
        self._logo_texture = None

    def _main(self) -> None:
        if self._logo_texture:
            imgui.image(
                self._logo_texture.texture_id,
                self._logo_texture.width,
                self._logo_texture.height,
            )

    def _process_window(self) -> None:
        viewport = imgui.get_main_viewport()
        pos_x, pos_y = viewport.work_pos
        size_x, size_y = viewport.work_size
        imgui.set_next_window_position(pos_x, pos_y)
        imgui.set_next_window_size(size_x, size_y)

        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0.0)
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.begin("Background Window", False, self._flags)
        imgui.pop_style_var(2)

        try:
            self._main()
        finally:
            imgui.end()

    @override
    def on_create(self) -> None:
        # logo_path = get_logos_path() / "logo.svg"
        # self._logo_texture = load_svg(logo_path, (256, 256))
        pass

    @override
    def on_destroy(self) -> None:
        pass

    @override
    def on_process(self) -> None:
        self._process_window()

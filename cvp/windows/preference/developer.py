# -*- coding: utf-8 -*-

import imgui

from cvp.logging.logging import logger
from cvp.types import override
from cvp.widgets.hoc.widget import WidgetInterface


class DeveloperPreference(WidgetInterface):
    def __init__(self, label="Developer"):
        self._section = self.propagated_context().config.developer
        self._label = label

    def __str__(self):
        return self._label

    @property
    def debug(self) -> bool:
        return self._section.debug

    @debug.setter
    def debug(self, value: bool):
        self._section.debug = value

    @property
    def verbose(self) -> int:
        return self._section.verbose

    @verbose.setter
    def verbose(self, value: int):
        self._section.verbose = value

    @override
    def on_process(self) -> None:
        debug_result = imgui.checkbox("Enable Debug Mode", self.debug)

        debug_changed = debug_result[0]
        debug_value = debug_result[1]
        assert isinstance(debug_value, bool)

        if debug_changed:
            self.debug = debug_value
            if debug_value:
                logger.info("Enabled debug mode")
            else:
                logger.info("Disabled debug mode")

        imgui.text("Verbose level:")
        verbose_result = imgui.input_int("##VerboseLevel", self.verbose)

        verbose_changed = verbose_result[0]
        verbose_value = verbose_result[1]
        assert isinstance(verbose_value, int)

        if verbose_changed:
            self.verbose = verbose_value
            logger.info(f"Changed verbose level: {verbose_value}")
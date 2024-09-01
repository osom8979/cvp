# -*- coding: utf-8 -*-

import os

import imgui

from cvp.config.sections.logging import LoggingSection
from cvp.logging.logging import (
    SEVERITIES,
    convert_level_number,
    loads_logging_config,
    logger,
    set_root_level,
)
from cvp.types import override
from cvp.widgets.hoc.widget import WidgetInterface


class LoggingPreference(WidgetInterface):
    def __init__(self, section: LoggingSection, label="Logging"):
        self._section = section
        self._label = label
        self._severities = list(SEVERITIES)

    def __str__(self):
        return self._label

    @property
    def config_path(self) -> str:
        return self._section.config_path

    @config_path.setter
    def config_path(self, value: str):
        self._section.config_path = value

    @property
    def root_severity(self) -> str:
        return self._section.root_severity

    @root_severity.setter
    def root_severity(self, value: str):
        self._section.root_severity = value

    @property
    def severity_index(self) -> int:
        try:
            return self._severities.index(self._section.root_severity)
        except ValueError:
            return -1

    @override
    def on_process(self) -> None:
        imgui.text("Logging json path:")
        logging_path_result = imgui.input_text(
            "##LoggingPath",
            self.config_path,
            -1,
            imgui.INPUT_TEXT_ENTER_RETURNS_TRUE,
        )

        logging_path_changed = logging_path_result[0]
        logging_path_value = logging_path_result[1]
        assert isinstance(logging_path_value, str)

        if logging_path_changed and os.path.isfile(logging_path_value):
            loads_logging_config(logging_path_value)
            logger.info(f"Loads the logging config file: '{logging_path_value}'")
            self.config_path = logging_path_value

        imgui.same_line()
        if imgui.button("Browse"):
            pass

        imgui.text("Root severity:")
        severity_result = imgui.combo(
            "##RootSeverity",
            self.severity_index,
            self._severities,
        )

        severity_changed = severity_result[0]
        severity_index = severity_result[1]
        assert isinstance(severity_index, int)

        if severity_changed and 0 <= severity_index < len(self._severities):
            severity_value = self._severities[severity_index]
            level = convert_level_number(severity_value)
            set_root_level(level)
            logger.log(level, f"Changed root severity: {severity_value}")
            self._section.root_severity = severity_value

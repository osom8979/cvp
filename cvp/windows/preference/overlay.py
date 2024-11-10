# -*- coding: utf-8 -*-

from typing import List

import imgui

from cvp.config.sections.overlay import Anchor
from cvp.context.context import Context
from cvp.logging.logging import logger
from cvp.types.override import override
from cvp.windows.preference._base import PreferenceWidget


class OverlayPreference(PreferenceWidget):
    _anchors: List[Anchor]

    def __init__(self, context: Context, label="Overlay"):
        self._config = context.config.overlay_window
        self._label = label
        self._anchors = list(Anchor)
        self._anchor_names = [str(a.name) for a in Anchor]
        self._anchor_index = self._anchors.index(self._config.anchor)

    @property
    @override
    def label(self) -> str:
        return self._label

    @override
    def on_process(self) -> None:
        imgui.text("Anchor:")
        anchor_result = imgui.combo("##Anchor", self._anchor_index, self._anchor_names)
        anchor_changed = anchor_result[0]
        if anchor_changed:
            anchor_index = anchor_result[1]
            assert isinstance(anchor_index, int)
            self._anchor_index = anchor_index
            self._config.anchor = self._anchors[anchor_index]

        imgui.text("Padding:")
        padding_result = imgui.input_int("##Padding", self._config.padding)
        padding_changed = padding_result[0]
        if padding_changed:
            padding_value = padding_result[1]
            assert isinstance(padding_value, int)
            self._config.padding = padding_value
            logger.info(f"Changed padding level: {padding_value}")

        imgui.text("Alpha:")
        alpha_result = imgui.slider_float(
            "##Alpha",
            self._config.alpha,
            0.0,
            1.0,
        )
        alpha_changed = alpha_result[0]
        if alpha_changed:
            alpha_value = alpha_result[1]
            assert isinstance(alpha_value, float)
            self._config.alpha = alpha_value
            logger.info(f"Changed alpha level: {alpha_value}")

        imgui.text("FPS Warning Threshold:")
        fps_warning_threshold_result = imgui.input_int(
            "##FPS Warning Threshold",
            self._config.fps_warning_threshold,
        )
        fps_warning_threshold_changed = fps_warning_threshold_result[0]
        fps_warning_threshold_value = fps_warning_threshold_result[1]
        assert isinstance(fps_warning_threshold_value, int)
        if fps_warning_threshold_changed:
            self._config.fps_warning_threshold = fps_warning_threshold_value
            logger.info(
                f"Changed fps_warning_threshold level: {fps_warning_threshold_value}"
            )

        imgui.text("FPS Error Threshold:")
        fps_error_threshold_result = imgui.input_int(
            "##FPS Error Threshold",
            self._config.fps_error_threshold,
        )
        fps_error_threshold_changed = fps_error_threshold_result[0]
        fps_error_threshold_value = fps_error_threshold_result[1]
        assert isinstance(fps_error_threshold_value, int)
        if fps_error_threshold_changed:
            self._config.fps_error_threshold = fps_error_threshold_value
            logger.info(
                f"Changed fps_error_threshold level: {fps_error_threshold_value}"
            )

        imgui.text("Normal Color:")
        normal_color_result = imgui.color_edit4(
            "##NormalColor",
            *self._config.normal_color,
        )
        normal_color_changed = normal_color_result[0]
        if normal_color_changed:
            normal_color_value = normal_color_result[1]
            assert isinstance(normal_color_value, tuple)
            assert len(normal_color_value) == 4
            self._config.normal_color = normal_color_value
            logger.info(f"Changed normal_color level: {normal_color_value}")

        imgui.text("Warning Color:")
        warning_color_result = imgui.color_edit4(
            "##WarningColor",
            *self._config.warning_color,
        )
        warning_color_changed = warning_color_result[0]
        if warning_color_changed:
            warning_color_value = warning_color_result[1]
            assert isinstance(warning_color_value, tuple)
            assert len(warning_color_value) == 4
            self._config.warning_color = warning_color_value
            logger.info(f"Changed warning_color level: {warning_color_value}")

        imgui.text("Error Color:")
        error_color_result = imgui.color_edit4(
            "##ErrorColor",
            *self._config.error_color,
        )
        error_color_changed = error_color_result[0]
        if error_color_changed:
            error_color_value = error_color_result[1]
            assert isinstance(error_color_value, tuple)
            assert len(error_color_value) == 4
            self._config.error_color = error_color_value
            logger.info(f"Changed error_color level: {error_color_value}")

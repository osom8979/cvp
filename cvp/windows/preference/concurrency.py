# -*- coding: utf-8 -*-

import imgui

from cvp.logging.logging import logger
from cvp.types import override
from cvp.widgets.hoc.widget import WidgetInterface


class ConcurrencyPreference(WidgetInterface):
    def __init__(self, label="Concurrency"):
        self._section = self.propagated_context().config.concurrency
        self._label = label
        self._show_restart = False

    def __str__(self):
        return self._label

    @property
    def thread_workers(self) -> int:
        return self._section.thread_workers

    @thread_workers.setter
    def thread_workers(self, value: int):
        self._section.thread_workers = value

    @property
    def process_workers(self) -> int:
        return self._section.process_workers

    @process_workers.setter
    def process_workers(self, value: int):
        self._section.process_workers = value

    @override
    def on_process(self) -> None:
        imgui.text("Thread workers:")
        thread_workers_result = imgui.input_int(
            "##ThreadWorkers",
            self.thread_workers,
        )

        thread_workers_changed = thread_workers_result[0]
        thread_workers_value = thread_workers_result[1]
        assert isinstance(thread_workers_value, int)

        if thread_workers_changed:
            self.thread_workers = thread_workers_value
            self._show_restart = True
            logger.info(f"Changed thread workers level: {thread_workers_value}")

        imgui.text("Process workers:")
        process_workers_result = imgui.input_int(
            "##ProcessWorkers",
            self.process_workers,
        )

        process_workers_changed = process_workers_result[0]
        process_workers_value = process_workers_result[1]
        assert isinstance(process_workers_value, int)

        if process_workers_changed:
            self.process_workers = process_workers_value
            self._show_restart = True
            logger.info(f"Changed process workers: {process_workers_value}")

        if self._show_restart:
            imgui.separator()
            imgui.text_colored("The change is applied after the start", 1.0, 0.1, 0.1)
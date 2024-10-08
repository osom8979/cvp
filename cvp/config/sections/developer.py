# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class DeveloperConfig:
    debug: bool = False
    verbose: int = 0

    show_metrics: bool = False
    show_style: bool = False
    show_demo: bool = False

    def flip_show_metrics(self) -> None:
        self.show_metrics = not self.show_metrics

    def flip_show_style(self) -> None:
        self.show_style = not self.show_style

    def flip_show_demo(self) -> None:
        self.show_demo = not self.show_demo

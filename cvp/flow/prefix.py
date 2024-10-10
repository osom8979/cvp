# -*- coding: utf-8 -*-

from enum import StrEnum, unique


@unique
class FlowPathPrefix(StrEnum):
    graph = "#"
    node = "@"
    pin = "+"
    arc = "~"

    graph_instance = "%"
    node_instance = "$"
    pin_instance = "*"
    arc_instance = "="

    reference = "&"

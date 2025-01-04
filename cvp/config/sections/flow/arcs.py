# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.variables import FLOW_ARCS_HOVERING_TOLERANCE


@dataclass
class Arcs:
    hovering_tolerance: float = FLOW_ARCS_HOVERING_TOLERANCE
